from copy import deepcopy

mat_grp_data = 'mat_grp_data'
material_group = 'material_group'
material_group_avg_count = 'material_group_avg_count'
mat_grp_year = 'mat_grp_year'
mat_grp_quarter = 'mat_grp_quarter'
mat_grp_month_name = 'mat_grp_month_name'
mat_grp_month = 'mat_grp_month'
material_group_yearly_list_ = "material_group_yearly_list"
distinct_material_groups = 'distinct_material_groups'
x_axis_labels = 'x_axis_labels'


def add_month_or_quarter_if_present(yearly_accumalator_list, each_material_group_data):
    data_dict = {}
    if each_material_group_data.get(mat_grp_month_name):
        data_dict = {material_group: each_material_group_data[material_group],
                     mat_grp_month_name: each_material_group_data[
                         mat_grp_month_name],
                     material_group_avg_count: each_material_group_data[
                         material_group_avg_count]}
    elif each_material_group_data.get(mat_grp_quarter):
        data_dict = {material_group: each_material_group_data[material_group],
                     mat_grp_quarter: each_material_group_data[
                         mat_grp_quarter],
                     material_group_avg_count: each_material_group_data[
                         material_group_avg_count]}
    else:
        data_dict = {material_group: each_material_group_data[material_group],
                     material_group_avg_count: each_material_group_data[
                         material_group_avg_count]}

    yearly_accumalator_list.append(deepcopy(data_dict))


def group_data_by_year(material_category_yqm_list_):
    try:
        distinct_material_group_list = []
        material_category_yqm_list = deepcopy(material_category_yqm_list_)
        material_group_yearly_list = []
        print(material_category_yqm_list)

        distinct_years_list = list(
            set(list(map(lambda each_data: each_data[mat_grp_year], material_category_yqm_list))))

        for each_distinct_year in distinct_years_list:
            yearly_accumalator_list = []
            for each_material_group_data in material_category_yqm_list:
                distinct_material_group_list.append(each_material_group_data[material_group])
                if each_material_group_data[mat_grp_year] == each_distinct_year:
                    add_month_or_quarter_if_present(yearly_accumalator_list, each_material_group_data)
            material_group_yearly_list.append({
                mat_grp_year: each_distinct_year,
                mat_grp_data: deepcopy(yearly_accumalator_list)
            })

        # print("Extected yearlt format")
        # print(material_group_yearly_list)
        return {"distinct_years": len(distinct_years_list), "distinct_years_list": distinct_years_list,
                material_group_yearly_list_: material_group_yearly_list,
                distinct_material_groups: list(set(distinct_material_group_list))}
    except Exception as e:
        print(e)
        return {"distinct_years": 0, "distinct_years_list": [],
                material_group_yearly_list_: [], distinct_material_groups: []}


def has_x_axis_label(x_axis_monthly_labels, x_axis_label):
    for current_x_axis in x_axis_monthly_labels:
        if current_x_axis == x_axis_label:
            return True
    return False


def group_data_by_month(material_category_monthly_result_list):
    try:
        yearly_data = group_data_by_year(material_category_monthly_result_list)
        print('group by year', yearly_data)
        material_group_monthly_list_local = deepcopy(yearly_data[material_group_yearly_list_])
        print("before dict ", material_group_monthly_list_local)
        month_dict = {
            "January": 1,
            "February": 2,
            "March": 3,
            "April": 4,
            "May": 5,
            "June": 6,
            "July": 7,
            "August": 8,
            "September": 9,
            "October": 10,
            "November": 11,
            "December": 12
        }

        distinct_material_group_list = deepcopy(yearly_data[distinct_material_groups])
        group_monthly_data_list_final = []

        x_axis_monthly_labels = []

        print("material_group_monthly_list_local")
        print(material_group_monthly_list_local)
        for each_year_data in material_group_monthly_list_local:
            distinct_months_for_year = list(
                set(list(map(lambda each_data: each_data[mat_grp_month_name], each_year_data[mat_grp_data]))))

            print("unsorted distinct month data", distinct_months_for_year)
            distinct_months_for_year.sort(key=lambda x: month_dict[x])

            group_monthly_data_list = []
            for each_month in distinct_months_for_year:
                monthly_data_accumulator = []
                x_axis_label = f'''{each_month} {each_year_data[mat_grp_year]}'''
                if not has_x_axis_label(x_axis_monthly_labels, x_axis_label):
                    x_axis_monthly_labels.append(x_axis_label)

                for mat_grp_data_local in each_year_data[mat_grp_data]:
                    if mat_grp_data_local[mat_grp_month_name] == each_month:
                        monthly_data_accumulator.append(mat_grp_data_local)

                group_monthly_data_list.append(
                    {mat_grp_month_name: each_month,
                     mat_grp_data: deepcopy(monthly_data_accumulator)})

            group_monthly_data_list_final.append({mat_grp_year: each_year_data[mat_grp_year],
                                                  "mat_grp_monthly_data": deepcopy(group_monthly_data_list)})
        print(group_monthly_data_list_final)
        return {"material_group_monthly_list": group_monthly_data_list_final,
                distinct_material_groups: distinct_material_group_list,
                x_axis_labels: list(x_axis_monthly_labels)}
    except Exception as e:
        print(e)
        return {"material_group_monthly_list": [], distinct_material_groups: [], x_axis_labels: []}


def group_data_by_quarter(material_category_quarterly_result_list):
    try:
        yearly_data = group_data_by_year(material_category_quarterly_result_list)
        material_group_quarterly_list_local = deepcopy(yearly_data[material_group_yearly_list_])
        distinct_material_group_list = deepcopy(yearly_data[distinct_material_groups])

        print("========= Quarterly data by group_by_year ============")
        print(material_group_quarterly_list_local)

        x_axis_quarterly_labels = []
        group_quarterly_data_list_final = []

        for each_year_data in material_group_quarterly_list_local:
            distinct_quarters_for_year = list(
                set(list(map(lambda each_data: each_data[mat_grp_quarter], each_year_data[mat_grp_data]))))
            group_quarterly_data_list = []
            for each_quarter in distinct_quarters_for_year:
                quarterly_data_accumulator = []
                x_axis_label = f'''Quarter {each_quarter} - {each_year_data[mat_grp_year]}'''
                if not has_x_axis_label(x_axis_quarterly_labels, x_axis_label):
                    x_axis_quarterly_labels.append(x_axis_label)

                for mat_grp_data_local in each_year_data[mat_grp_data]:
                    if mat_grp_data_local[mat_grp_quarter] == each_quarter:
                        quarterly_data_accumulator.append(mat_grp_data_local)

                group_quarterly_data_list.append(
                    {mat_grp_quarter: each_quarter,
                     mat_grp_data: deepcopy(quarterly_data_accumulator)})

            group_quarterly_data_list_final.append({mat_grp_year: each_year_data[mat_grp_year],
                                                    "mat_grp_quarterly_data": deepcopy(group_quarterly_data_list)})

        print("Material category quarterly list")
        print(group_quarterly_data_list_final)
        return {"material_group_quarterly_list": group_quarterly_data_list_final,
                distinct_material_groups: distinct_material_group_list,
                x_axis_labels: list(x_axis_quarterly_labels)}
    except Exception as e:
        print(e)
        return {"material_group_quarterly_list": [], distinct_material_groups: [], x_axis_labels: []}


def group_data_by_semi(material_category_monthly_result_list):
    try:
        yearly_data = group_data_by_year(material_category_monthly_result_list)
        material_group_monthly_list_local = deepcopy(yearly_data[material_group_yearly_list_])
        distinct_material_group_list = deepcopy(yearly_data[distinct_material_groups])
        group_monthly_data_list_final = []

        x_axis_monthly_labels = []

        print("material_group_monthly_list_local")
        print(material_group_monthly_list_local)
        for each_year_data in material_group_monthly_list_local:
            distinct_months_for_year = list(
                set(list(map(lambda each_data: each_data[mat_grp_month_name], each_year_data[mat_grp_data]))))
            group_monthly_data_list = []
            for each_month in distinct_months_for_year:
                monthly_data_accumulator = []
                x_axis_label = f'''Half {each_month} {each_year_data[mat_grp_year]}'''
                if not has_x_axis_label(x_axis_monthly_labels, x_axis_label):
                    x_axis_monthly_labels.append(x_axis_label)

                for mat_grp_data_local in each_year_data[mat_grp_data]:
                    if mat_grp_data_local[mat_grp_month_name] == each_month:
                        monthly_data_accumulator.append(mat_grp_data_local)

                group_monthly_data_list.append(
                    {mat_grp_month_name: each_month,
                     mat_grp_data: deepcopy(monthly_data_accumulator)})

            group_monthly_data_list_final.append({mat_grp_year: each_year_data[mat_grp_year],
                                                  "mat_grp_monthly_data": deepcopy(group_monthly_data_list)})
        print(group_monthly_data_list_final)
        return {"material_group_monthly_list": group_monthly_data_list_final,
                distinct_material_groups: distinct_material_group_list,
                x_axis_labels: list(x_axis_monthly_labels)}
    except Exception as e:
        print(e)
        return {"material_group_monthly_list": [], distinct_material_groups: [], x_axis_labels: []}


# Litter index helpers

litterassessment_year = 'litterassessment_year'
litterassessment_quarter = 'litterassessment_quarter'
litterassessment_semi_annually = 'litterassessment_semi_annually'
litterassessment = 'litterassessment'
litterassessment_month = 'litterassessment_month'
distinct_plu = 'distinct_plu'
plu = 'plu'
breaking_point = 999999999


def group_litter_index_by_year(litter_index_yearly_data):
    x_axis_labels_list = []
    distinct_plu_list = []
    current_year = ''
    response_data = []
    temp_response_data_accumulator = []
    litter_index_yearly_data.append({"breaking_point_": breaking_point})
    try:
        for each_year_litter_index in litter_index_yearly_data:
            # stop collectoion and grouping by year if breaking point is reached and clean up
            if each_year_litter_index.get("breaking_point_"):
                response_data.append({litterassessment_year: current_year
                                         , "data_for_year": deepcopy(temp_response_data_accumulator)})
                temp_response_data_accumulator.clear()
                break

            # Deleting county key as its not needed in output
            # if each_year_litter_index.get('county'):
            if each_year_litter_index.get('county'):
                del each_year_litter_index['county']

            # Collect distinct plus
            distinct_plu_list.append(each_year_litter_index[plu])

            # collect distinct years for x_axis_labels
            if each_year_litter_index[litterassessment_year] not in x_axis_labels_list:
                x_axis_labels_list.append(each_year_litter_index[litterassessment_year])

            if current_year == '':
                current_year = each_year_litter_index[litterassessment_year]
                temp_response_data_accumulator.append(each_year_litter_index)

            elif current_year != '' and current_year != each_year_litter_index[litterassessment_year]:
                print(each_year_litter_index[litterassessment_year])
                response_data.append({litterassessment_year: current_year
                                         , "data_for_year": deepcopy(temp_response_data_accumulator)})
                temp_response_data_accumulator.clear()
                current_year = each_year_litter_index[litterassessment_year]
                temp_response_data_accumulator.append(each_year_litter_index)

            else:
                temp_response_data_accumulator.append(each_year_litter_index)

        return {x_axis_labels: x_axis_labels_list,
                distinct_plu: list(set(distinct_plu_list)),
                'litter_index_yearly_data': response_data}

    except Exception as e:
        print(e)
        return {x_axis_labels: [],
                distinct_plu: [],
                'litter_index_yearly_data': []}


def group_litter_index_by_year_single(litter_index_yearly_data, single_key):
    x_axis_labels_list = []
    distinct_plu_list = []
    print('yearly', litter_index_yearly_data)
    current_year = ''
    response_data = []
    temp_response_data_accumulator = []
    litter_index_yearly_data.append({"breaking_point_": breaking_point})

    try:
        for each_year_litter_index in litter_index_yearly_data:
            # stop collectoion and grouping by year if breaking point is reached and clean up
            if each_year_litter_index.get("breaking_point_"):
                response_data.append({litterassessment_year: current_year
                                         , "data_for_year": deepcopy(temp_response_data_accumulator)})
                temp_response_data_accumulator.clear()
                break

            # Deleting county key as its not needed in output
            # if each_year_litter_index.get('county'):
            #    del each_year_litter_index['county']

            # Collect distinct plus
            # distinct_plu_list.append("ALL")

            # collect distinct years for x_axis_labels
            if each_year_litter_index[litterassessment_year] not in x_axis_labels_list:
                x_axis_labels_list.append(each_year_litter_index[litterassessment_year])

            if current_year == '':
                current_year = each_year_litter_index[litterassessment_year]
                each_year_litter_index['plu'] = single_key
                temp_response_data_accumulator.append(each_year_litter_index)

            elif current_year != '' and current_year != each_year_litter_index[litterassessment_year]:
                print(each_year_litter_index[litterassessment_year])
                response_data.append({litterassessment_year: current_year
                                         , "data_for_year": deepcopy(temp_response_data_accumulator)})
                temp_response_data_accumulator.clear()
                current_year = each_year_litter_index[litterassessment_year]
                each_year_litter_index['plu'] = single_key
                temp_response_data_accumulator.append(each_year_litter_index)

            else:
                temp_response_data_accumulator.append(each_year_litter_index)
        print('response', {x_axis_labels: x_axis_labels_list,
                           distinct_plu: [single_key],
                           'litter_index_yearly_data': response_data})
        return {x_axis_labels: x_axis_labels_list,
                distinct_plu: [single_key],
                'litter_index_yearly_data': response_data}

    except Exception as e:
        print(e)
        return {x_axis_labels: [],
                distinct_plu: [],
                'litter_index_yearly_data': []}


# year_parts or part_years indicated the data either belongs to monthly_grouping or quarterly_group
# below is a generic function to group data by either month or quarter
# for_quarter param is set by the caller view function to tell below function to group by month or quarter
def group_litter_index_by_year_parts_single(litter_index_monthly_or_monthly_data, single_key, for_quarter=False,
                                            semi_annually=False):
    # Initially group data for month or quarter by year
    litter_index_yearly_data = group_litter_index_by_year_single(litter_index_monthly_or_monthly_data, single_key)

    # extract distinct plus
    distinct_plu_list = litter_index_yearly_data[distinct_plu]

    litter_index_yearly_data = litter_index_yearly_data['litter_index_yearly_data']
    x_axis_labels_list = []
    response_data = []

    # decide for what to group data by month or quarter
    # if for_quarter is True then need to group by quarter else by month
    part_year_key = litterassessment_month
    data_for_key = 'data_for_month'
    litter_index_response_data_key = 'litter_index_monthly_data'
    if for_quarter:
        part_year_key = litterassessment_quarter
        data_for_key = 'data_for_quarter'
        litter_index_response_data_key = 'litter_index_quarterly_data'

    if semi_annually:
        part_year_key = litterassessment_semi_annually
        data_for_key = 'data_for_semi_annually'
        litter_index_response_data_key = 'litter_index_semi_annually'

    try:

        print("----------------- Keys ----------------")
        print(part_year_key)
        print(data_for_key)
        print(litter_index_response_data_key)

        for each_year_litter_index in litter_index_yearly_data:
            temp_response_data_accumulator = []
            # print("-------  each_year_data ------------")
            # print(each_year_litter_index)
            current_year = each_year_litter_index[litterassessment_year]
            data_list_for_current_year = each_year_litter_index['data_for_year']
            # print(current_year)

            current_part_year = ''
            part_year_accumulator_data = []
            data_list_for_current_year.append({"breaking_point_": breaking_point})
            for each_part_year_litter_index in data_list_for_current_year:

                # stop collection and grouping by year if breaking point is reached and clean up
                if each_part_year_litter_index.get("breaking_point_"):
                    part_year_accumulator_data.append({part_year_key: current_part_year
                                                          , data_for_key: deepcopy(temp_response_data_accumulator)})
                    temp_response_data_accumulator.clear()
                    break

                # collect year-month pair for x_axis_labels
                if not for_quarter and not semi_annually:
                    if f'''{'' if part_year_key == litterassessment_semi_annually else ''}{each_part_year_litter_index[part_year_key]} - {current_year}''' not in x_axis_labels_list:
                        x_axis_labels_list.append(
                            f'''{'' if part_year_key == litterassessment_semi_annually else ''}{each_part_year_litter_index[part_year_key]} - {current_year}''')

                elif for_quarter and f'''{'Q' if part_year_key == litterassessment_quarter else ''}{each_part_year_litter_index[part_year_key]} - {current_year}''' not in x_axis_labels_list:
                    x_axis_labels_list.append(
                        f'''{'Q' if part_year_key == litterassessment_quarter else ''}{each_part_year_litter_index[part_year_key]} - {current_year}''')

                elif semi_annually and f'''{'Half ' if part_year_key == litterassessment_semi_annually else ''}{each_part_year_litter_index[part_year_key]} - {current_year}''' not in x_axis_labels_list:
                    x_axis_labels_list.append(
                        f'''{'Half ' if part_year_key == litterassessment_semi_annually else ''}{each_part_year_litter_index[part_year_key]} - {current_year}''')

                if current_part_year == '':
                    current_part_year = each_part_year_litter_index[part_year_key]
                    each_part_year_litter_index['plu'] = single_key
                    temp_response_data_accumulator.append(each_part_year_litter_index)

                elif current_part_year != '' and current_part_year != each_part_year_litter_index[part_year_key]:
                    part_year_accumulator_data.append({part_year_key: current_part_year
                                                          , data_for_key: deepcopy(temp_response_data_accumulator)})
                    temp_response_data_accumulator.clear()
                    current_part_year = each_part_year_litter_index[part_year_key]
                    each_part_year_litter_index['plu'] = single_key
                    temp_response_data_accumulator.append(each_part_year_litter_index)

                else:
                    temp_response_data_accumulator.append(each_part_year_litter_index)

            # populate_missing_plu(part_year_accumulator_data, distinct_plu_list, data_for_key)

            sub_part_year_key = 'monthly_data'
            if for_quarter:
                sub_part_year_key = 'quarterly_data'
            elif semi_annually:
                sub_part_year_key = 'semi_annually_data'

            response_data.append({litterassessment_year: current_year,
                                  sub_part_year_key: deepcopy(
                                      part_year_accumulator_data),
                                  })

        return {x_axis_labels: x_axis_labels_list, litter_index_response_data_key: response_data,
                distinct_plu: distinct_plu_list, 'for_quarter': for_quarter, 'semi_annually': semi_annually}

    except:
        print("Exception in group_litter_index_by_year_parts_single")
        return {x_axis_labels: [], litter_index_response_data_key: [],
                distinct_plu: [], 'for_quarter': for_quarter, 'semi_annually': semi_annually}


# year_parts or part_years indicated the data either belongs to monthly_grouping or quarterly_group
# below is a generic function to group data by either month or quarter
# for_quarter param is set by the caller view function to tell below function to group by month or quarter
def group_litter_index_by_year_parts(litter_index_monthly_or_monthly_data, for_quarter=False, semi_annually=False):
    # Initially group data for month or quarter by year
    litter_index_yearly_data = group_litter_index_by_year(litter_index_monthly_or_monthly_data)

    # extract distinct plus
    distinct_plu_list = litter_index_yearly_data[distinct_plu]

    litter_index_yearly_data = litter_index_yearly_data['litter_index_yearly_data']
    x_axis_labels_list = []
    response_data = []

    # decide for what to group data by month or quarter
    # if for_quarter is True then need to group by quarter else by month
    part_year_key = litterassessment_month
    data_for_key = 'data_for_month'
    litter_index_response_data_key = 'litter_index_monthly_data'
    if for_quarter:
        part_year_key = litterassessment_quarter
        data_for_key = 'data_for_quarter'
        litter_index_response_data_key = 'litter_index_quarterly_data'

    if semi_annually:
        part_year_key = litterassessment_semi_annually
        data_for_key = 'data_for_semi_annually'
        litter_index_response_data_key = 'litter_index_semi_annually'

    try:

        print("----------------- Keys ----------------")
        print(part_year_key)
        print(data_for_key)
        print(litter_index_response_data_key)

        for each_year_litter_index in litter_index_yearly_data:
            temp_response_data_accumulator = []
            # print("-------  each_year_data ------------")
            # print(each_year_litter_index)
            current_year = each_year_litter_index[litterassessment_year]
            data_list_for_current_year = each_year_litter_index['data_for_year']
            # print(current_year)

            current_part_year = ''
            part_year_accumulator_data = []
            data_list_for_current_year.append({"breaking_point_": breaking_point})
            for each_part_year_litter_index in data_list_for_current_year:

                # stop collection and grouping by year if breaking point is reached and clean up
                if each_part_year_litter_index.get("breaking_point_"):
                    part_year_accumulator_data.append({part_year_key: current_part_year
                                                          , data_for_key: deepcopy(temp_response_data_accumulator)})
                    temp_response_data_accumulator.clear()
                    break

                # collect year-month pair for x_axis_labels
                if not for_quarter and not semi_annually:
                    if f'''{'' if part_year_key == litterassessment_semi_annually else ''}{each_part_year_litter_index[part_year_key]} - {current_year}''' not in x_axis_labels_list:
                        x_axis_labels_list.append(
                            f'''{'' if part_year_key == litterassessment_semi_annually else ''}{each_part_year_litter_index[part_year_key]} - {current_year}''')

                elif for_quarter and f'''{'Q' if part_year_key == litterassessment_quarter else ''}{each_part_year_litter_index[part_year_key]} - {current_year}''' not in x_axis_labels_list:
                    x_axis_labels_list.append(
                        f'''{'Q' if part_year_key == litterassessment_quarter else ''}{each_part_year_litter_index[part_year_key]} - {current_year}''')

                elif semi_annually and f'''{'Half ' if part_year_key == litterassessment_semi_annually else ''}{each_part_year_litter_index[part_year_key]} - {current_year}''' not in x_axis_labels_list:
                    x_axis_labels_list.append(
                        f'''{'Half ' if part_year_key == litterassessment_semi_annually else ''}{each_part_year_litter_index[part_year_key]} - {current_year}''')

                if current_part_year == '':
                    current_part_year = each_part_year_litter_index[part_year_key]
                    temp_response_data_accumulator.append(each_part_year_litter_index)

                elif current_part_year != '' and current_part_year != each_part_year_litter_index[part_year_key]:
                    part_year_accumulator_data.append({part_year_key: current_part_year
                                                          , data_for_key: deepcopy(temp_response_data_accumulator)})
                    temp_response_data_accumulator.clear()
                    current_part_year = each_part_year_litter_index[part_year_key]
                    temp_response_data_accumulator.append(each_part_year_litter_index)

                else:
                    temp_response_data_accumulator.append(each_part_year_litter_index)

            populate_missing_plu(part_year_accumulator_data, distinct_plu_list, data_for_key)

            sub_part_year_key = 'monthly_data'
            if for_quarter:
                sub_part_year_key = 'quarterly_data'
            elif semi_annually:
                sub_part_year_key = 'semi_annually_data'

            response_data.append({litterassessment_year: current_year,
                                  sub_part_year_key: deepcopy(
                                      part_year_accumulator_data),
                                  })

        print("Returning")
        print({x_axis_labels: x_axis_labels_list, litter_index_response_data_key: response_data,
               distinct_plu: distinct_plu_list, 'for_quarter': for_quarter, 'semi_annually': semi_annually})

        return {x_axis_labels: x_axis_labels_list, litter_index_response_data_key: response_data,
                distinct_plu: distinct_plu_list, 'for_quarter': for_quarter, 'semi_annually': semi_annually}

    except:
        print("Exception in single part year")
        return {x_axis_labels: [], litter_index_response_data_key: [],
                distinct_plu: [], 'for_quarter': for_quarter, 'semi_annually': semi_annually}


def has_plu(data_list, plu_):
    for each_data in data_list:
        if each_data[plu] == plu_:
            return True
    return False


def populate_missing_plu(data_list, distinct_plu_, data_for_key):
    print(data_list)
    for each_plu in distinct_plu_:
        for each_data_item in data_list:
            if not has_plu(each_data_item[data_for_key], each_plu):
                each_data_item[data_for_key].append({plu: each_plu, litterassessment: None})
