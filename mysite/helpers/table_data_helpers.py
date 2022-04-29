def get_chart_data_query(request):
    data = request.GET
    shed = data.get('shed')
    board = data.get('board')
    county = data.get('countyname')
    city = data.get('cityname')
    fromdate = data.get('frdate')
    todate = data.get('tdate')
    pname = data.getlist('plname[]')
    if pname is not None and "ALL" in pname:
        pname.remove("ALL")
    permitteenum = data.get('permitten')

    query_prefix = '''
                   select  CONVERT(varchar, creation_date, 102) as date,
                           TRADE.record_trashitem.material_group,
                           TRADE.record_trashitem.itemcount,
                           TRADE.record_trashitem.material_category 
                           from
                           TRADE.record_main
                           INNER JOIN
                           TRADE.record_trashitem 
                           ON TRADE.record_main.RecordID = TRADE.record_trashitem.recordid 
                   '''

    if permitteenum:
        if permitteenum == "ALL":
            return f'''{query_prefix}
                    where
                    CAST(creation_date as DATE) between '{fromdate}' and '{todate}' '''
        else:
            return f'''{query_prefix}
                    where
                    TRADE.record_main.permittee = '{permitteenum}' and 
                    CAST(creation_date as DATE) between '{fromdate}' and '{todate}' 
                    and TRADE.record_main.plu in ('{"','".join([str(ele) for ele in pname])}') '''
    elif city:
        if city == "ALL":
            return f'''{query_prefix} 
                        where
                        CAST(creation_date as DATE) between '{fromdate}' and '{todate}' '''
        else:
            return f'''{query_prefix} 
                        where
                        TRADE.record_main.city = '{city}'
                        and CAST(creation_date as DATE) between '{fromdate}' and '{todate}' '''
    elif county:
        if county == "ALL":
            return f'''{query_prefix} 
                        where
                        CAST(creation_date as DATE) between '{fromdate}' and '{todate}' '''
        else:
            return f'''{query_prefix}
                        where
                        TRADE.record_main.county = '{county}' 
                        and CAST(creation_date as DATE) between '{fromdate}' and '{todate}' '''

    elif shed:
        if shed == "ALL":
            return f'''{query_prefix} 
                        where
                        CAST(creation_date as DATE) between '{fromdate}' and '{todate}' '''
        else:
            return f'''{query_prefix}
                    where
                    TRADE.record_main.Watershed_Name = '{shed}'
                    and CAST(creation_date as DATE) between '{fromdate}' and '{todate}' '''
    elif board:
        if board == "ALL":
            return f'''{query_prefix} 
                        where
                        CAST(creation_date as DATE) between '{fromdate}' and '{todate}' '''
        else:
            return f'''{query_prefix}
                    where
                    TRADE.record_main.Waterboard_Name = '{board}'
                    and CAST(creation_date as DATE) between '{fromdate}' and '{todate}' '''


def _create_part_year_query(getFor=3, forGroupBy=False, isAllSelected=False):
    comma = " " if isAllSelected else ","

    print("Comma ->", comma)

    base_select_col = 'Datepart(year, TempTable.date) AS litterassessment_year ' + comma
    base_group_by_col = 'Datepart(year, TempTable.date)' + comma

    if getFor == 3:
        if forGroupBy:
            return base_group_by_col
        return base_select_col

    elif getFor == 2:
        if forGroupBy:
            return f'''
            {base_group_by_col} {"," if comma == " " else ""}
            Datepart(QUARTER, TempTable.date) {comma}
            '''
        else:
            return f'''
            {base_select_col}{"," if comma == " " else ""}
            Datepart(QUARTER, TempTable.date) AS litterassessment_quarter {comma}
            '''
    elif getFor == 1:
        if forGroupBy:
            return f'''
            {base_group_by_col}{"," if comma == " " else ""}
             MONTH(TempTable.date),
             DateName( MONTH , DateAdd( month , Datepart(MONTH, TempTable.date) , 0 ) - 1 ){comma}
            '''
        else:
            return f'''
            {base_select_col}{"," if comma == " " else ""}
            DateName( MONTH , DateAdd( MONTH , Datepart(MONTH, TempTable.date) , 0 ) - 1 ) AS litterassessment_month {comma}
            '''

    else:
        if forGroupBy:
            return f'''
            {base_group_by_col}{"," if comma == " " else ""}
             ( ( Month(TempTable.date) - 1 ) / 6 ) + 1 {comma}
            '''
        else:
            return f'''
            {base_select_col}{"," if comma == " " else ""}
            ( ( Month(TempTable.date) - 1 ) / 6 ) + 1 AS litterassessment_semi_annually{comma}
            '''


def get_litter_index_data(request, getFor=0):
    data = request.GET
    pname = data.getlist('plname[]')
    shed = data.get('shed')
    board = data.get('board')
    county = data.get('countyname')
    city = data.get('cityname')
    fromdate = data.get('frdate')
    todate = data.get('tdate')
    if pname is not None and "ALL" in pname:
        pname.remove("ALL")
    permitteenum = data.get('permitten')
    if permitteenum:
        if permitteenum == "ALL":
            return f'''SELECT
                            Avg(Cast(TempTable.litterassessment as Float)) AS litterassessment,
                            {_create_part_year_query(getFor, isAllSelected=True)}
                            FROM(
                                SELECT CONVERT(VARCHAR, creation_date, 102) AS date,
                                   trade.record_main.litterassessment      
                            FROM   trade.record_main 
                            WHERE  CAST(creation_date as DATE) between '{fromdate}' and '{todate}')
                        TempTable
                        GROUP  BY  
                        {_create_part_year_query(getFor, forGroupBy=True, isAllSelected=True)}
                        order by Datepart(year, TempTable.date)
            '''
        else:
            return f'''
                    SELECT Cast(TempTable.plu AS VARCHAR(100)) AS plu,
                    
                    Avg(Cast(TempTable.litterassessment as Float))  AS litterassessment,
                    {_create_part_year_query(getFor)}
                    Cast(TempTable.permittee AS VARCHAR(100))
                    FROM(
                       SELECT CONVERT(VARCHAR, creation_date, 102) AS date,
                       trade.record_main.litterassessment,
                       trade.record_main.plu,
                       trade.record_main.permittee 
                FROM   trade.record_main
                WHERE  {"" if permitteenum == "ALL" else "TRADE.record_main.permittee = '" + permitteenum + "' and "} 
                       CAST(creation_date as DATE) between '{fromdate}' and '{todate}' 
                       AND TRADE.record_main.plu in ('{"','".join([str(ele) for ele in pname])}'))
                TempTable 
                GROUP  BY
                Cast(TempTable.permittee AS VARCHAR(100)),
                          
                {_create_part_year_query(getFor, forGroupBy=True)}
                Cast(TempTable.plu AS VARCHAR(100))
                order by Datepart(year, TempTable.date) 
    '''
    elif city:
        if city == "ALL":
            return f'''
                    SELECT
                        Avg(Cast(TempTable.litterassessment as Float)) AS litterassessment,
                        {_create_part_year_query(getFor, isAllSelected=True)}
                        FROM(
                            SELECT CONVERT(VARCHAR, creation_date, 102) AS date,
                               trade.record_main.litterassessment
                        FROM   trade.record_main
                        WHERE  CAST(creation_date as DATE) between '{fromdate}' and '{todate}')
                    TempTable
                    GROUP  BY  
                    {_create_part_year_query(getFor, forGroupBy=True, isAllSelected=True)}
                    order by Datepart(year, TempTable.date)
        '''
        else:
            print('city litter',city)
            return f'''
                        SELECT
                            Avg(Cast(TempTable.litterassessment as Float)) AS litterassessment,
                            {_create_part_year_query(getFor, isAllSelected=True)}
                             FROM
                                (SELECT CONVERT(VARCHAR, creation_date, 102) AS date,
                                   trade.record_main.litterassessment 
                                   FROM   trade.record_main
                                   WHERE  TRADE.record_main.city = '{city}'
                                   AND CAST(creation_date as DATE) between '{fromdate}' and '{todate}')
                                   TempTable
                            GROUP  BY  
                            {_create_part_year_query(getFor, forGroupBy=True, isAllSelected=True)} 
                            order by Datepart(year, TempTable.date)'''


    elif county:
        if county== "ALL":
            return f'''
                    SELECT
                        Avg(Cast(TempTable.litterassessment as Float)) AS litterassessment,
                        {_create_part_year_query(getFor, isAllSelected=True)}
                        FROM(
                            SELECT CONVERT(VARCHAR, creation_date, 102) AS date,
                               trade.record_main.litterassessment 
                        FROM   trade.record_main
                        WHERE  CAST(creation_date as DATE) between '{fromdate}' and '{todate}')
                    TempTable
                    GROUP  BY  
                    {_create_part_year_query(getFor, forGroupBy=True, isAllSelected=True)}
                    order by Datepart(year, TempTable.date)
        '''
        else:
            return f'''
                        SELECT
                        Avg(Cast(TempTable.litterassessment as Float))                       AS litterassessment,
                        {_create_part_year_query(getFor, isAllSelected=True)}
                        FROM (
                           SELECT CONVERT(VARCHAR, creation_date, 102) AS date,
                           trade.record_main.litterassessment 
                    FROM   trade.record_main
                    WHERE  TRADE.record_main.county = '{county}' 
                           AND CAST(creation_date as DATE) between '{fromdate}' and '{todate}')
                    TempTable
                    GROUP BY
                    {_create_part_year_query(getFor, forGroupBy=True, isAllSelected=True)}
                     order by Datepart(year, TempTable.date)
                    '''


    elif shed:
        if shed == "ALL":
            return f'''
                    SELECT
                        Avg(Cast(TempTable.litterassessment as Float)) AS litterassessment,
                        {_create_part_year_query(getFor, isAllSelected=True)}
                        FROM(
                            SELECT CONVERT(VARCHAR, creation_date, 102) AS date,
                               trade.record_main.litterassessment 
                        FROM   trade.record_main
                        WHERE  CAST(creation_date as DATE) between '{fromdate}' and '{todate}')
                    TempTable
                    GROUP  BY  
                    {_create_part_year_query(getFor, forGroupBy=True, isAllSelected=True)}
                    order by Datepart(year, TempTable.date)
        '''
        else:
            return f'''
                    SELECT
                        Avg(Cast(TempTable.litterassessment as Float)) AS litterassessment,
                        {_create_part_year_query(getFor, isAllSelected=True)}
                         FROM
                            (SELECT CONVERT(VARCHAR, creation_date, 102) AS date,
                               trade.record_main.litterassessment 
                               FROM   trade.record_main
                               WHERE  TRADE.record_main.Watershed_Name = '{shed}'
                               AND CAST(creation_date as DATE) between '{fromdate}' and '{todate}')
                               TempTable
                        GROUP  BY  
                        {_create_part_year_query(getFor, forGroupBy=True, isAllSelected=True)} 
                        order by Datepart(year, TempTable.date)'''
    elif board:
        if board == "ALL":
            return f'''
                    SELECT
                        Avg(Cast(TempTable.litterassessment as Float)) AS litterassessment,
                        {_create_part_year_query(getFor, isAllSelected=True)}
                        FROM(
                            SELECT CONVERT(VARCHAR, creation_date, 102) AS date,
                               trade.record_main.litterassessment 
                        FROM   trade.record_main
                        WHERE  CAST(creation_date as DATE) between '{fromdate}' and '{todate}')
                    TempTable
                    GROUP  BY  
                    {_create_part_year_query(getFor, forGroupBy=True, isAllSelected=True)}
                    order by Datepart(year, TempTable.date)
        '''
        else:
            return f'''
                    SELECT
                        Avg(Cast(TempTable.litterassessment as Float)) AS litterassessment,
                        {_create_part_year_query(getFor, isAllSelected=True)}
                         FROM
                            (SELECT CONVERT(VARCHAR, creation_date, 102) AS date,
                               trade.record_main.litterassessment
                               FROM   trade.record_main
                               WHERE  TRADE.record_main.Waterboard_Name = '{board}'
                               AND CAST(creation_date as DATE) between '{fromdate}' and '{todate}')
                               TempTable
                        GROUP  BY  
                        {_create_part_year_query(getFor, forGroupBy=True, isAllSelected=True)} 
                        order by Datepart(year, TempTable.date)'''
