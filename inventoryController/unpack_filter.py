from CCPDController.utils import (
    sanitizeString, 
    sanitizeNumber, 
    full_iso_format,
    inv_iso_format
)
from datetime import datetime, timedelta

# 
def unpackTimeRange(query_filter, fil, query_key, filter_name, t_format="%Y-%m-%dT%H:%M:%S.000Z"):
    # time range filter
    if query_key in query_filter:
        timeRange = query_filter[query_key]

        selectValue = timeRange['selectValue'] if 'selectValue' in timeRange else ''
        if selectValue == 'today' or selectValue == 'yesterday':
            # time range selection dropdown value from panel
            if selectValue == 'today':
                fil[filter_name] = {
                    '$gte': datetime.now().replace(hour=0, minute=0, second=0).strftime(t_format),
                    '$lt': datetime.now().replace(hour=23, minute=59, second=59).strftime(t_format)
                }
            elif selectValue == 'yesterday':
                fil[filter_name] = {
                    '$gte': (datetime.now() - timedelta(1)).replace(hour=0, minute=0, second=0).strftime(t_format),
                    '$lt': (datetime.now() - timedelta(1)).replace(hour=23, minute=59, second=59).strftime(t_format)
                }
            # elif selectValue == 'thisWeek':
            #     fil[filter_name] = {
            #         '$gte': (datetime.now() - timedelta(7)).replace(hour=0, minute=0, second=0).strftime(t_format),
            #         '$lt': datetime.now().replace(hour=23, minute=59, second=59).strftime(t_format),
            #     }
            # elif selectValue == 'thisMonth':
            #     fil[filter_name] = {
            #         '$gte': datetime.now().replace(day=1, hour=0, minute=0, second=0).strftime(t_format),
            #         '$lt': datetime.now().replace(hour=23, minute=59, second=59).strftime(t_format),
            #     }
        
        if ('from' in timeRange and timeRange['from'] != '') or ('to' in timeRange and timeRange['to'] != ''):
            f = sanitizeString(timeRange['from']) if 'from' in timeRange else ''

            if f != '':
                f = datetime.strptime(f, full_iso_format).strftime(t_format)
                
            # selected only 1 day so range is from 0000 to 2359 of that day
            if 'to' not in timeRange and 'from' in timeRange:
                t = datetime.strptime(f, t_format).replace(hour=23, minute=59, second=59).strftime(t_format)
            # both to and from are in filter
            elif 'to' in timeRange and 'from' in timeRange:
                t = datetime.strptime(sanitizeString(timeRange['to']), full_iso_format).replace(hour=23, minute=59, second=59).strftime(t_format)
            
            # populate time filter in fil object
            fil[filter_name] = {
                '$gte': f,
                '$lt': t
            }
            
def unpackQAFilter(query_filter, fil, key):
    # qa personal filter
    if 'qaFilter' in query_filter and len(query_filter['qaFilter']) > 0:
        qaf = { '$or': [] }
        for name in query_filter['qaFilter']:
            n = sanitizeString(name)
            qaf['$or'].append({ f'{key}': n })
        fil['$and'].append(qaf)

def unpackSkuFilter(query_filter, fil):
    if 'targetSku' in query_filter and query_filter['targetSku'] != '':
        sku = {'sku': sanitizeNumber(int(query_filter['targetSku']))}
        fil['$and'].append(sku)
    elif 'sku' in query_filter: 
        sku = {'sku': {}}
        if 'gte' in query_filter['sku'] and query_filter['sku']['gte'] != '':
            sku['sku']['$gte'] = sanitizeNumber(int(query_filter['sku']['gte']))
        if 'lte' in query_filter['sku'] and query_filter['sku']['lte'] != '':
            sku['sku']['$lte'] = sanitizeNumber(int(query_filter['sku']['lte']))
        if sku != {'sku': {}}:
            fil['$and'].append(sku)

def unpackPlatformFilter(query_filter, fil):
    # original platform filter
    if 'platformFilter' in query_filter and query_filter['platformFilter'] != '':
        sanitizeString(query_filter['platformFilter'])
        fil['$and'].append({'platform': query_filter['platformFilter']})

def unpackMarketPlaceFilter(query_filter, fil): 
        # marketplace filter
    if 'marketplaceFilter' in query_filter and query_filter['marketplaceFilter'] != '':
        sanitizeString(query_filter['marketplaceFilter'])
        fil['$and'].append({'marketplace': query_filter['marketplaceFilter']})

def unpackShelfLocation(query_filter, fil):
    # shelf location Filter
    if 'shelfLocationFilter' in query_filter and len(query_filter['shelfLocationFilter']) > 0:
        shf = { '$or': [] }
        for loc in query_filter['shelfLocationFilter']:
            l = sanitizeString(loc)
            shf['$or'].append({ 'shelfLocation': l })
        fil['$and'].append(shf)

# unpack Q&A Record filter object passed in by frontend
def unpackQARecordFilter(query_filter, fil):
    # create $and array
    if '$and' not in fil:
        fil['$and'] = []
    
    # item condition filter
    if 'conditionFilter' in query_filter and query_filter['conditionFilter'] != '':
        sanitizeString(query_filter['conditionFilter'])
        fil['$and'].append({'itemCondition': query_filter['conditionFilter']})
    
    if 'showRecordedOnly' in query_filter and query_filter['showRecordedOnly'] == True:
        fil['$and'].append({'recorded': True})
    
    unpackMarketPlaceFilter(query_filter, fil)
    unpackPlatformFilter(query_filter, fil)
    unpackTimeRange(query_filter, fil, 'timeRangeFilter', 'time')
    unpackSkuFilter(query_filter, fil)
    unpackShelfLocation(query_filter, fil)
    unpackQAFilter(query_filter, fil, 'ownerName')
    
    # keyword filter on comment and link
    if 'keywordFilter' in query_filter and len(query_filter['keywordFilter']) > 0:
        kwFilter = { '$or': [] }
        for word in query_filter['keywordFilter']:
            keyword = sanitizeString(word)
            kwFilter['$or'].append({ 'comment': {'$regex': keyword} })
            kwFilter['$or'].append({ 'link': {'$regex': keyword} })
        fil['$and'].append(kwFilter)
    
    # remove $and if no filter applied
    if fil['$and'] == []:
        del fil['$and']
    return fil

# unpack instock inventory filter object passed in by frontend
def unpackInstockFilter(query_filter, fil):
    # instock filter
    if 'instockFilter' in query_filter:
        sanitizeString(query_filter['instockFilter'])
        match query_filter['instockFilter']:
            case 'in':
                fil['quantityInstock'] = { '$gt': 0 }
            case 'out':
                fil['quantityInstock'] = { '$lte': 0 }
            case '':
                pass
    
    # create $and array
    if '$and' not in fil:
        fil['$and'] = []
    
    # sku filter
    unpackSkuFilter(query_filter, fil)
    
    # item condition filter
    if 'conditionFilter' in query_filter and query_filter['conditionFilter'] != '':
        sanitizeString(query_filter['conditionFilter'])
        fil['$and'].append({'condition': query_filter['conditionFilter']})
    
    # admin filter
    if 'adminFilter' in query_filter and len(query_filter['adminFilter']) > 0:
        adf = { '$or': [] }
        for name in query_filter['adminFilter']:
            n = sanitizeString(name)
            adf['$or'].append({ 'adminName': n })
        fil['$and'].append(adf)
    
    # keyword filter on lead and description
    if 'keywordFilter' in query_filter and len(query_filter['keywordFilter']) > 0:
        kwFilter = { '$or': [] }
        for word in query_filter['keywordFilter']:
            keyword = sanitizeString(word)
            kwFilter['$or'].append({ 'lead': {'$regex': keyword} })
            kwFilter['$or'].append({ 'description': {'$regex': keyword} })
        fil['$and'].append(kwFilter)
    
    # msrp filter
    if 'msrpFilter' in query_filter:
        msrpFilter = query_filter['msrpFilter']
        if msrpFilter['gte'] != '' or msrpFilter['lt'] != '':
            fil['msrp'] = {}
            if msrpFilter['gte'] != '':
                fil['msrp']['$gte'] = float(msrpFilter['gte'])
            if msrpFilter['lt'] != '': 
                fil['msrp']['$lt'] = float(msrpFilter['lt'])
    
    unpackPlatformFilter(query_filter, fil)
    unpackMarketPlaceFilter(query_filter, fil)
    unpackShelfLocation(query_filter, fil)
    unpackTimeRange(query_filter, fil, 'timeRangeFilter', 'time')
    unpackTimeRange(query_filter, fil, 'qaTime', 'qaTime')
    unpackQAFilter(query_filter, fil, 'qaName')
    
    # remove $and if no filter applied
    # $and cannot be empty
    if fil['$and'] == []:
        del fil['$and']
    return fil