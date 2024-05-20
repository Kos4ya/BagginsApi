import pandas as pd
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from .core import transform_data
from .models import Point
from catboost import CatBoostRegressor


class GetPointView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    @staticmethod
    def is_xlsx(filename):
        return filename.split('.')[-1] == 'xlsx'

    def get(self, request, id):
        if not self.request.data.get('dates'):
            return Response({"message": "Поле dates обязательно и должно хранить дату в формате YYYY-MM-DD"},
                            status=status.HTTP_400_BAD_REQUEST)
        dates_list = self.request.data.get('dates').split()
        point = get_object_or_404(Point, id=id)
        model_turnover = point.model_turnover.path
        model_order = point.model_order.path
        file = request.FILES['file']
        df_weather = pd.read_excel(file)
        df = transform_data(df_weather)
        data = {}
        data['turnovers'] = []
        data['orders'] = []
        model1 = CatBoostRegressor()
        model2 = CatBoostRegressor()

        model_turnover = model1.load_model(model_turnover)
        model_order = model2.load_model(model_order)
        dates_list = [pd.to_datetime(date).date() for date in dates_list]

        for date in dates_list:
            row = df[df['time'].dt.date == date]
            if not row.empty:
                features = row[
                    ['T', 'Po', 'Pa', 'U', 'DD', 'Ff', 'Nh', 'VV', 'RRR', 'cloud', 'year', 'month', 'day',
                     'day_of_week', 'is_holiday']].values

                predicted_orders = model_order.predict(features)[0]
                data['orders'].append({"date": date, "predict": predicted_orders})
                predicted_turnovers = model_turnover.predict(features)[0]
                data['turnovers'].append({"date": date, "predict": predicted_turnovers})

        return Response(data, status=status.HTTP_200_OK)


class GetPointTurnoverView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, id):
        if not self.request.data.get('dates'):
            return Response({"message": "Поле dates обязательно и должно хранить дату в формате YYYY-MM-DD"},
                            status=status.HTTP_400_BAD_REQUEST)
        dates_list = self.request.data.get('dates').split()
        point = get_object_or_404(Point, id=id)
        model_turnover = point.model_turnover.path
        file = request.FILES['file']
        df_weather = pd.read_excel(file)
        df = transform_data(df_weather)
        data = {}
        data['orders'] = []
        model = CatBoostRegressor()

        model_turnover = model.load_model(model_turnover)
        dates_list = [pd.to_datetime(date).date() for date in dates_list]

        for date in dates_list:
            row = df[df['time'].dt.date == date]
            if not row.empty:
                features = row[
                    ['T', 'Po', 'Pa', 'U', 'DD', 'Ff', 'Nh', 'VV', 'RRR', 'cloud', 'year', 'month', 'day',
                     'day_of_week', 'is_holiday']].values
                predicted_turnovers = model_turnover.predict(features)[0]
                data['turnovers'].append({"date": date, "predict": predicted_turnovers})

        return Response(data, status=status.HTTP_200_OK)


class GetPointOrderView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, id):
        if not self.request.data.get('dates'):
            return Response({"message": "Поле dates обязательно и должно хранить дату в формате YYYY-MM-DD"},
                            status=status.HTTP_400_BAD_REQUEST)
        dates_list = self.request.data.get('dates').split()
        point = get_object_or_404(Point, id=id)
        model_order = point.model_order.path
        file = request.FILES['file']
        df_weather = pd.read_excel(file)
        df = transform_data(df_weather)
        data = {}
        data['orders'] = []
        model = CatBoostRegressor()

        model_order = model.load_model(model_order)
        dates_list = [pd.to_datetime(date).date() for date in dates_list]

        for date in dates_list:
            row = df[df['time'].dt.date == date]
            if not row.empty:
                features = row[
                    ['T', 'Po', 'Pa', 'U', 'DD', 'Ff', 'Nh', 'VV', 'RRR', 'cloud', 'year', 'month', 'day',
                     'day_of_week', 'is_holiday']].values

                predicted_orders = model_order.predict(features)[0]
                data['orders'].append({"date": date, "predict": predicted_orders})

        return Response(data, status=status.HTTP_200_OK)
