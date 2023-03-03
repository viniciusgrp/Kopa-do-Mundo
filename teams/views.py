from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Team
from django.forms.models import model_to_dict
from teams.utils import ImpossibleTitlesError, InvalidTitles, InvalidYearCupError, NegativeTitlesError, data_processing, validate_titles, validate_wins, validate_year

# Create your views here.
class TeamDontExists(Exception):
    ...


class TeamView(APIView):
    def post(self, request):
        team_data = request.data    

        try:
            validate_titles(team_data['titles'])
            validate_year(team_data['first_cup'])
            validate_wins(team_data['titles'], team_data['first_cup'])
        except NegativeTitlesError as err:
            return Response({'error': err.message}, 400)
        except InvalidYearCupError as err:
            return Response({'error': err.message}, 400)
        except ImpossibleTitlesError as err:
            return Response({'error': err.message}, 400)

        team = Team.objects.create(**team_data)

        return Response(model_to_dict(team), 201)


    
    def get(self, request):
        teams = Team.objects.all()

        teams_dict = []

        for team in teams:
            dict_team = model_to_dict(team)
            teams_dict.append(dict_team)

        return Response(teams_dict)


class TeamDetailView(APIView):
    def get(self, request, team_id):
        try:
            team = Team.objects.get(id=team_id)

            return Response(model_to_dict(team), 200)
        except Team.DoesNotExist:
            return Response({"message": "Team not found"}, 404)

    
    def delete(self, request, team_id: int):
        try:
            team = Team.objects.get(id=team_id)

            print(team)

            team.delete()
            return Response(status=204)

        except Team.DoesNotExist:
            return Response({"message": "Team not found"}, 404)
        

    def patch(self, request, team_id):
        try:
            team = Team.objects.get(id=team_id)

            for key, value in request.data.items():
                setattr(team, key, value)

            team.save()

            return Response(model_to_dict(team), 200)

        except Team.DoesNotExist:
            return Response({"message": "Team not found"}, 404)