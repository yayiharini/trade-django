from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from django.core.files.storage import default_storage
import pyodbc
from django.shortcuts import render
from django.http import HttpResponse
import json
from Trade.models import *
from helpers import helpers
from helpers import table_data_helpers

# DB_STRING = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=aa1alz8o7yyog2a.cd5eunuhsflb.us-west-2.rds.amazonaws.com,1433;DATABASE=TradeDB;uid=hariniyayi;pwd=hariniyayi;'
DB_STRING = 'Driver= {ODBC Driver 17 for SQL Server};SERVER=UL-ARC1003-1416;DATABASE=TradeDB;UID=project_user;PWD=project_password;Trusted_Connection=yes;'


def create_connection():
    conn = pyodbc.connect(
        DB_STRING
    )
    return conn


conn = create_connection()


@api_view(['GET', 'POST'])
def consql(request):
    cursor = conn.cursor()
    cursor.execute("select distinct plu from TRADE.record_main")
    result = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    print(columns)
    items = []
    for row in result:
        item = dict(zip(columns, row))
        print(item)
        items.append(item)
    return Response(items)


@api_view(['GET'])
def getcitycounty(request):
    cursor = conn.cursor()
    cursor.execute("select distinct city,county from TRADE.record_main")
    result = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    print(columns)
    items = []
    for row in result:
        item = dict(zip(columns, row))
        print(item)
        items.append(item)
    print(json.dumps(items))
    return Response(items)


@api_view(['GET'])
def getwatershed(request):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("select distinct HUC8_code,Watershed_Name from TRADE.record_main")
    result = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    print(columns)
    items = []
    for row in result:
        item = dict(zip(columns, row))
        print(item)
        items.append(item)
    print(json.dumps(items))
    return Response(items)


@api_view(['GET'])
def getwaterboard(request):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("select distinct Waterboard_Name from TRADE.record_main")
    result = cursor.fetchall()

    columns = [column[0] for column in cursor.description]
    print(columns)
    items = []
    for row in result:
        item = dict(zip(columns, row))
        print(item)
        items.append(item)
    print(json.dumps(items))
    return Response(items)


@api_view(['GET'])
def getpermitte(request):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("select distinct permittee from TRADE.record_main where permittee != '' ")
    result = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    print(columns)
    items = []
    for row in result:
        item = dict(zip(columns, row))
        print(item)
        items.append(item)
    print(json.dumps(items))
    return Response(items)


@api_view(['GET'])
def get_material_group_count(request):
    print('request', request.GET)
    sub_query = table_data_helpers.get_chart_data_query(request)
    cursor = conn.cursor()
    final_query = f'''select
                       CAST(TempTable.material_group AS VARCHAR(100)) as material_group,
                       SUM(TempTable.itemcount) as material_group_count 
                        from
                           ( {sub_query} )
                           TempTable 
                        GROUP BY
                       CAST( TempTable.material_group AS VARCHAR(100)) '''
    print(final_query)
    material_group_count_list = []
    for row in cursor.execute(final_query):
        item = dict(zip(["material_group", "material_group_count"], row))
        material_group_count_list.append(item)
    print(material_group_count_list)
    return Response({"pieChartData": material_group_count_list})


# Sub pie chart data
@api_view(['GET'])
def get_material_category_data(request):
    sub_query = table_data_helpers.get_chart_data_query(request)
    data = request.GET
    print(request.data)
    material_group = data.get('material_group')
    cursor = conn.cursor()
    material_category_query = f'''select
                                       SUM(TempTable.itemcount) as itemcount,
                                       CAST(TempTable.material_category AS VARCHAR(100)) as material_category 
                                        from
                                           ( {sub_query} )
                                           TempTable 
                                        where
                                           CAST(TempTable.material_group AS VARCHAR(100)) = '{material_group}' 
                                        GROUP BY
                                           CAST(TempTable.material_category AS VARCHAR(100)) '''

    material_category_list = []
    for row in cursor.execute(material_category_query):
        item = dict(zip(["itemcount", "material_category"], row))
        material_category_list.append(item)
    print('material cat', material_category_list)
    return Response(
        {"subPieChartData": {"material_group": material_group, "material_category_list": material_category_list}})


@api_view(['GET'])
def get_material_group_yearly_data(request):
    sub_query = table_data_helpers.get_chart_data_query(request)
    material_group_yearly_data_query = f'''SELECT Cast(TempTable.material_group AS VARCHAR(100)) AS material_group,
                                                   LOG(Avg(TempTable.itemcount))   AS material_group_avg_count,
                                                   Datepart(year, TempTable.date)   AS mat_grp_year
                                                FROM   ({sub_query}) TempTable
                                                GROUP  BY Datepart(year, TempTable.date),
                                                          Cast(TempTable.material_group AS VARCHAR(100))
                                                ORDER BY mat_grp_year ASC '''
    print(material_group_yearly_data_query)
    cursor = conn.cursor()
    material_category_yqm_list = []
    for row in cursor.execute(material_group_yearly_data_query):
        item = dict(zip(["material_group", "material_group_avg_count", "mat_grp_year"], row))
        material_category_yqm_list.append(item)

    return Response({"material_group_yearly_data": helpers.group_data_by_year(material_category_yqm_list)})


@api_view(['GET'])
def get_material_group_monthly_data(request):
    sub_query = table_data_helpers.get_chart_data_query(request)
    material_group_monthly_data_query = f'''SELECT Cast(TempTable.material_group AS VARCHAR(100)) AS material_group,
                                                         LOG(Avg(TempTable.itemcount))  AS material_group_avg_count,
                                                         DATENAME(MONTH, TempTable.date)   AS mat_grp_month_name,       
                                                         MONTH(TempTable.date)  AS mat_grp_month,
                                                         YEAR(TempTable.date)  AS mat_grp_year
                                                  FROM   ({sub_query}) TempTable
                                                  GROUP  BY YEAR(TempTable.date),
                                                            MONTH(TempTable.date),
                                                            DATENAME(MONTH, TempTable.date),
                                                            Cast(TempTable.material_group AS VARCHAR(100))
                                                  ORDER BY mat_grp_year ASC'''

    print('material group query', material_group_monthly_data_query)

    cursor = conn.cursor()
    material_category_monthly_result_list = []
    for row in cursor.execute(material_group_monthly_data_query):
        item = dict(
            zip(["material_group", "material_group_avg_count", "mat_grp_month_name", "mat_grp_month",
                 "mat_grp_year"],
                row))
        material_category_monthly_result_list.append(item)
    print('monthly list', material_category_monthly_result_list)
    print("month", helpers.group_data_by_month(material_category_monthly_result_list))
    return Response({"material_group_monthly_data": helpers.group_data_by_month(material_category_monthly_result_list)})


@api_view(['GET'])
def get_material_group_quarterly_data(request):
    sub_query = table_data_helpers.get_chart_data_query(request)
    material_group_quarterly_data_query = f'''SELECT Cast(TempTable.material_group AS VARCHAR(100)) AS material_group,
                                                   LOG(Avg(TempTable.itemcount))  AS material_group_avg_count,
                                                   Datepart(QUARTER, TempTable.date) AS mat_grp_quarter,
                                                   Datepart(year, TempTable.date) AS mat_grp_year
                                            FROM   ({sub_query}) TempTable
                                            GROUP  BY Datepart(year, TempTable.date),
                                                      Datepart(QUARTER, TempTable.date),
                                                      Cast(TempTable.material_group AS VARCHAR(100))
                                            ORDER BY mat_grp_year ASC'''

    cursor = conn.cursor()
    material_category_quarterly_result_list = []
    for row in cursor.execute(material_group_quarterly_data_query):
        item = dict(
            zip(["material_group", "material_group_avg_count", "mat_grp_quarter",
                 "mat_grp_year"],
                row))
        material_category_quarterly_result_list.append(item)
    return Response(
        {"material_group_quarterly_data": helpers.group_data_by_quarter(material_category_quarterly_result_list)})


@api_view(['GET'])
def get_material_group_semianually_data(request):
    print("hi")
    sub_query = table_data_helpers.get_chart_data_query(request)
    material_group_monthly_data_query = f'''SELECT Cast(TempTable.material_group AS VARCHAR(100)) AS material_group,
                                                         LOG(Avg(TempTable.itemcount))  AS material_group_avg_count,
                                                         ( ( Month(TempTable.date) - 1 ) / 6 ) + 1   AS mat_grp_month_name,       
                                                         ( ( Month(TempTable.date) - 1 ) / 6 ) + 1  AS mat_grp_month,
                                                         YEAR(TempTable.date)  AS mat_grp_year
                                                  FROM   ({sub_query}) TempTable
                                                  GROUP  BY YEAR(TempTable.date),
                                                            ( ( Month(TempTable.date) - 1 ) / 6 ) + 1,
                                                            DATENAME(MONTH, TempTable.date),
                                                            Cast(TempTable.material_group AS VARCHAR(100))
                                                  ORDER BY mat_grp_year ASC'''

    cursor = conn.cursor()
    material_category_monthly_result_list = []
    for row in cursor.execute(material_group_monthly_data_query):
        item = dict(
            zip(["material_group", "material_group_avg_count", "mat_grp_month_name", "mat_grp_month",
                 "mat_grp_year"],
                row))
        material_category_monthly_result_list.append(item)
    print("month", material_category_monthly_result_list)
    return Response({"material_group_monthly_data": helpers.group_data_by_semi(material_category_monthly_result_list)})


# Sub line chart views
@api_view(['GET'])
def get_sub_line_chart_yearly_data(request):
    sub_query = table_data_helpers.get_chart_data_query(request)
    material_group_in_request = request.GET.get('material_group')
    material_group_yearly_data_query = f'''SELECT Cast(TempTable.material_category AS VARCHAR(100)) AS material_group,
                                                LOG(Avg(TempTable.itemcount))  AS material_group_avg_count,
                                                Datepart(year, TempTable.date) AS mat_grp_year
                                                FROM   ({sub_query}) TempTable
                                                WHERE Cast(TempTable.material_group AS VARCHAR(100)) = '{material_group_in_request}'
                                                GROUP  BY Datepart(year, TempTable.date),
                                                          Cast(TempTable.material_category AS VARCHAR(100))
                                                ORDER BY mat_grp_year ASC '''
    print(material_group_yearly_data_query)
    cursor = conn.cursor()
    material_group_yqm_list = []
    for row in cursor.execute(material_group_yearly_data_query):
        item = dict(zip(["material_group", "material_group_avg_count", "mat_grp_year"], row))
        material_group_yqm_list.append(item)

    return Response({"material_group_yearly_data": helpers.group_data_by_year(material_group_yqm_list)})


@api_view(['GET'])
def get_sub_line_chart_quarterly_data(request):
    sub_query = table_data_helpers.get_chart_data_query(request)
    material_group_in_request = request.GET.get('material_group')
    material_group_quarterly_data_query = f'''SELECT Cast(TempTable.material_category AS VARCHAR(100)) AS material_group,
                                                       LOG(Avg(TempTable.itemcount))  AS material_group_avg_count,
                                                       Datepart(QUARTER, TempTable.date) AS mat_grp_quarter,
                                                       Datepart(year, TempTable.date) AS mat_grp_year
                                                FROM   ({sub_query}) TempTable
                                                WHERE Cast(TempTable.material_group AS VARCHAR(100)) = '{material_group_in_request}' 
                                                GROUP  BY Datepart(year, TempTable.date),
                                                          Datepart(QUARTER, TempTable.date),
                                                          Cast(TempTable.material_category AS VARCHAR(100))
                                                ORDER BY mat_grp_year ASC'''

    cursor = conn.cursor()
    material_category_quarterly_result_list = []
    for row in cursor.execute(material_group_quarterly_data_query):
        item = dict(
            zip(["material_group", "material_group_avg_count", "mat_grp_quarter",
                 "mat_grp_year"],
                row))
        material_category_quarterly_result_list.append(item)
    return Response(
        {"material_group_quarterly_data": helpers.group_data_by_quarter(material_category_quarterly_result_list)})


@api_view(['GET'])
def get_sub_line_chart_monthly_data(request):
    sub_query = table_data_helpers.get_chart_data_query(request)
    material_group_in_request = request.GET.get('material_group')
    material_group_monthly_data_query = f'''SELECT Cast(TempTable.material_category AS VARCHAR(100)) AS material_group,
                                                         LOG(Avg(TempTable.itemcount))  AS material_group_avg_count,
                                                         DATENAME(MONTH, TempTable.date)   AS mat_grp_month_name,       
                                                         MONTH(TempTable.date)  AS mat_grp_month,
                                                         YEAR(TempTable.date)  AS mat_grp_year
                                                  FROM   ({sub_query}) TempTable
                                                  WHERE Cast(TempTable.material_group AS VARCHAR(100)) = '{material_group_in_request}'
                                                  GROUP  BY YEAR(TempTable.date),
                                                            MONTH(TempTable.date),
                                                            DATENAME(MONTH, TempTable.date),
                                                            Cast(TempTable.material_category AS VARCHAR(100))
                                                  ORDER BY mat_grp_year ASC'''

    cursor = conn.cursor()
    material_category_monthly_result_list = []
    for row in cursor.execute(material_group_monthly_data_query):
        item = dict(
            zip(["material_group", "material_group_avg_count", "mat_grp_month_name", "mat_grp_month",
                 "mat_grp_year"],
                row))
        material_category_monthly_result_list.append(item)

    return Response({"material_group_monthly_data": helpers.group_data_by_month(material_category_monthly_result_list)})


@api_view(['GET'])
def get_sub_line_chart_semianual_data(request):
    sub_query = table_data_helpers.get_chart_data_query(request)
    material_group_in_request = request.GET.get('material_group')
    print('material group', material_group_in_request)
    material_group_monthly_data_query = f'''SELECT Cast(TempTable.material_category AS VARCHAR(100)) AS material_group,
                                                         LOG(Avg(TempTable.itemcount))  AS material_group_avg_count,
                                                         ( ( Month(TempTable.date) - 1 ) / 6 ) + 1   AS mat_grp_month_name,       
                                                        ( ( Month(TempTable.date) - 1 ) / 6 ) + 1  AS mat_grp_month,
                                                         YEAR(TempTable.date)  AS mat_grp_year
                                                  FROM   ({sub_query}) TempTable
                                                  WHERE Cast(TempTable.material_group AS VARCHAR(100)) = '{material_group_in_request}'
                                                  GROUP  BY YEAR(TempTable.date),
                                                            ( ( Month(TempTable.date) - 1 ) / 6 ) + 1,
                                                            DATENAME(MONTH, TempTable.date),
                                                            Cast(TempTable.material_category AS VARCHAR(100))
                                                  ORDER BY mat_grp_year ASC'''

    cursor = conn.cursor()
    material_category_monthly_result_list = []
    for row in cursor.execute(material_group_monthly_data_query):
        item = dict(
            zip(["material_group", "material_group_avg_count", "mat_grp_month_name", "mat_grp_month",
                 "mat_grp_year"],
                row))
        material_category_monthly_result_list.append(item)

    return Response({"material_group_monthly_data": helpers.group_data_by_semi(material_category_monthly_result_list)})


@api_view(['GET'])
def getrecords(request):
    data = request.GET
    shed = data.get('shed')
    board = data.get('board')
    county = data.get('countyname')
    city = data.get('cityname')
    fromdate = data.get('frdate')
    todate = data.get('tdate')
    pname = data.getlist('plname[]')
    if "ALL" in pname:
        pname.remove("ALL")
    permitteenum = data.get('permitten')
    cursor = conn.cursor()
    q = ""
    query_prefix = '''
                 select 
                    CONVERT(varchar, creation_date, 102) as date, 
                    RecordMain.LitterAssessment as LitterAssessment,
                    RecordMain.plu as plu, 
                    RecordMain.permittee as permittee,
                    RecordMain.location_name as location, 
                    RecordMain.x_value as x,
                    RecordMain.y_value as y,
                    RecordMain.RecordId as recid,
				    (select
				    STRING_AGG(TRADE.trashitem.material_group,',') 
				    from TRADE.trashitem
				    where TRADE.trashitem.recordid = RecordMain.RecordID)
				    as material_group,
				    (select SUM(TRADE.trashitem.itemcount)as itemcount 
                     from TRADE.trashitem
				    where TRADE.trashitem.recordid = RecordMain.RecordID
                    ) as itemcount
                    from TRADE.record_main as RecordMain  
                    where   
    '''
    if permitteenum:
        if permitteenum == "ALL":
            q = f'''{query_prefix}
                 CAST(creation_date as DATE) between '{fromdate}' and '{todate}'  '''
        else:
            q = f'''{query_prefix}
                RecordMain.permittee = '{permitteenum}' and
                CAST(creation_date as DATE) between '{fromdate}' and '{todate}' 
                and RecordMain.plu in ('{"','".join([str(ele) for ele in pname])}') '''
    elif city:
        if city == "ALL":
            print("entered city all")
            q = f''' {query_prefix}
                CAST(creation_date as DATE) between '{fromdate}' and '{todate}' '''
        else:
            print('enter', city)
            q = f'''{query_prefix} 
                    RecordMain.city = '{city}' 
                    and CAST(creation_date as DATE) between '{fromdate}' and '{todate}' '''
            print(q)
    elif county:
        if county == "ALL":
            print("entered all")
            q = f'''{query_prefix} 
                    CAST(creation_date as DATE) between '{fromdate}' and '{todate}' '''
        else:
            q = f'''{query_prefix} 
                    RecordMain.county = '{county}' 
                    and CAST(creation_date as DATE) between '{fromdate}' and '{todate}' '''
    elif shed:
        if shed == "ALL":
            print("entered all")
            q = f'''{query_prefix} 
                    CAST(creation_date as DATE) between '{fromdate}' and '{todate}' '''
        else:
            q = f''' {query_prefix}
                RecordMain.Watershed_Name = '{shed}' 

                and CAST(creation_date as DATE) between '{fromdate}' and '{todate}' '''
    elif board:
        if board == "ALL":
            print("entered all")
            q = f'''{query_prefix} 
                    CAST(creation_date as DATE) between '{fromdate}' and '{todate}' '''
        else:
            q = f''' {query_prefix}
                RecordMain.Waterboard_Name = '{board}' 

                and CAST(creation_date as DATE) between '{fromdate}' and '{todate}' '''
    result = cursor.execute(q)

    print(result)
    columns = [column[0] for column in cursor.description]
    items = []
    for row in result:
        item = dict(zip(columns, row))
        items.append(item)
    print(json.dumps({"tableData": items}))
    json.dumps(items, indent=4, sort_keys=True, default=str)
    return Response({"tableData": items})


@api_view(['POST'])
def getplu(request):
    conn = create_connection()
    data = request.data
    data = data.get('data')
    permittee = data.get('permitte')
    print(permittee)
    cursor = conn.cursor()
    if permittee == 'ALL':
        cursor.execute("select distinct plu from TRADE.record_main where plu != ''")
    else:
        cursor.execute("select distinct plu from TRADE.record_main where plu != '' and permittee='" + permittee + "'")
    result = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    print(columns)
    items = []
    for row in result:
        item = dict(zip(columns, row))
        print(item)
        items.append(item)
    print(json.dumps(items))
    return Response(items)


@api_view(['GET'])
def get_litter_index_yearly_data(request):
    subquery = table_data_helpers.get_litter_index_data(request, getFor=3)
    print("---------- get_litter_index_yearly_data ------------")
    print(subquery)
    cursor = conn.cursor()
    cursor.execute(subquery)
    result = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    items = []
    for row in result:
        item = dict(zip(columns, row))
        items.append(item)

    data = request.GET
    permitteenum = data.get('permitten')
    shed = data.get('shed')
    board = data.get('board')
    county = data.get('countyname')
    city = data.get('cityname')
    if city:
        print("Single city value average")
        return Response(helpers.group_litter_index_by_year_single(items, city))
    elif county:
        print("Single value average county")
        return Response(helpers.group_litter_index_by_year_single(items, county))
    elif shed:
        print("Single value average shed")
        return Response(helpers.group_litter_index_by_year_single(items, shed))
    elif board:
        print("Single value average")
        return Response(helpers.group_litter_index_by_year_single(items, board))
    elif permitteenum == "ALL":
        return Response(helpers.group_litter_index_by_year_single(items, "ALL PERMITEES"))

    return Response(helpers.group_litter_index_by_year(items))


@api_view(['GET'])
def get_litter_index_monthly_data(request):
    sub_query = table_data_helpers.get_litter_index_data(request, getFor=1)
    print("---------- get_litter_index_monthly_data ------------")
    print(sub_query)
    cursor = conn.cursor()
    cursor.execute(sub_query)
    result = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    items = []
    for row in result:
        item = dict(zip(columns, row))
        items.append(item)
    data = request.GET
    permitteenum = data.get('permitten')
    shed = data.get('shed')
    board = data.get('board')
    county = data.get('countyname')
    city = data.get('cityname')
    print('items', items)
    if city:
        print("Single city value average")
        return Response(helpers.group_litter_index_by_year_parts_single(items, city))
    elif county:
        print("Single value average")
        return Response(helpers.group_litter_index_by_year_parts_single(items, county))
    elif shed:
        print("Single value average")
        return Response(helpers.group_litter_index_by_year_parts_single(items, shed))
    elif board:
        print("Single value average")
        return Response(helpers.group_litter_index_by_year_parts_single(items, board))
    elif permitteenum == "ALL":
        print(helpers.group_litter_index_by_year_parts_single(items, "ALL PERMITIEES"))
        return Response(helpers.group_litter_index_by_year_parts_single(items, "ALL PERMITIEES"))
    return Response(helpers.group_litter_index_by_year_parts(items))


@api_view(['GET'])
def get_litter_index_quarterly_data(request):
    sub_query = table_data_helpers.get_litter_index_data(request, getFor=2)
    print("---------- get_litter_index_quarterly_data ------------")
    print(sub_query)
    cursor = conn.cursor()
    cursor.execute(sub_query)
    result = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    items = []
    for row in result:
        item = dict(zip(columns, row))
        items.append(item)
    data = request.GET
    permitteenum = data.get('permitten')
    shed = data.get('shed')
    board = data.get('board')
    county = data.get('countyname')
    city = data.get('cityname')
    if city:
        print("Single city value average")
        return Response(helpers.group_litter_index_by_year_parts_single(items, city, for_quarter=True))
    elif county:
        print("Single value average")
        return Response(helpers.group_litter_index_by_year_parts_single(items, county, for_quarter=True))
    elif shed:
        print("Single value average")
        return Response(helpers.group_litter_index_by_year_parts_single(items, shed, for_quarter=True))
    elif board:
        print("Single value average")
        return Response(helpers.group_litter_index_by_year_parts_single(items, board, for_quarter=True))
    elif permitteenum == "ALL":
        print(helpers.group_litter_index_by_year_parts_single(items, "ALL PERMITIEES", for_quarter=True))
        return Response(helpers.group_litter_index_by_year_parts_single(items, "ALL PERMITIEES", for_quarter=True))

    print(helpers.group_litter_index_by_year_parts(items, for_quarter=True))
    return Response(helpers.group_litter_index_by_year_parts(items, for_quarter=True))


@api_view(['GET'])
def get_litter_index_semi_annually_data(request):
    sub_query = table_data_helpers.get_litter_index_data(request, getFor=0)
    print("---------- get_litter_index_semi_annually_datagetLineChartDataByYear ------------")
    print(sub_query)
    cursor = conn.cursor()
    cursor.execute(sub_query)
    result = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    items = []
    for row in result:
        item = dict(zip(columns, row))
        items.append(item)
    data = request.GET
    permitteenum = data.get('permitten')
    shed = data.get('shed')
    board = data.get('board')
    county = data.get('countyname')
    city = data.get('cityname')
    if city:
        print("Single city value average")
        return Response(helpers.group_litter_index_by_year_parts_single(items, city, semi_annually=True))
    elif county:
        print("Single value average")
        return Response(helpers.group_litter_index_by_year_parts_single(items, county, semi_annually=True))
    elif shed:
        print("Single value average")
        return Response(helpers.group_litter_index_by_year_parts_single(items, shed, semi_annually=True))
    elif board:
        print("Single value average")
        return Response(helpers.group_litter_index_by_year_parts_single(items, board, semi_annually=True))

    elif permitteenum == "ALL":
        print(helpers.group_litter_index_by_year_parts_single(items, "ALL PERMITIEES", semi_annually=True))
        return Response(helpers.group_litter_index_by_year_parts_single(items, "ALL PERMITIEES", semi_annually=True))

    print(helpers.group_litter_index_by_year_parts(items, semi_annually=True))
    return Response(helpers.group_litter_index_by_year_parts(items, semi_annually=True))


