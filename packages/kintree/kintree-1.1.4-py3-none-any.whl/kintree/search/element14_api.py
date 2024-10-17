from ..config import settings, config_interface
from ..common.tools import download

ELEMENT14_API_URL = 'https://api.element14.com/catalog/products'

STORES = {
    'Farnell': {
        'Bulgaria': 'bg.farnell.com ',
        'Czechia': 'cz.farnell.com',
        'Denmark': 'dk.farnell.com',
        'Austria': 'at.farnell.com ',
        'Switzerland': 'ch.farnell.com',
        'Germany': 'de.farnell.com',
        'CPC UK': 'cpc.farnell.com',
        'CPC Ireland': 'cpcireland.farnell.com',
        'Export': 'export.farnell.com',
        'Onecall': 'onecall.farnell.com',
        'Ireland': 'ie.farnell.com',
        'Israel': 'il.farnell.com',
        'United Kingdom': 'uk.farnell.com',
        'Spain': 'es.farnell.com',
        'Estonia': 'ee.farnell.com',
        'Finland': 'fi.farnell.com',
        'France': 'fr.farnell.com',
        'Hungary': 'hu.farnell.com',
        'Italy': 'it.farnell.com',
        'Lithuania': 'lt.farnell.com',
        'Latvia': 'lv.farnell.com',
        'Belgium': 'be.farnell.com',
        'Netherlands': 'nl.farnell.com',
        'Norway': 'no.farnell.com',
        'Poland': 'pl.farnell.com',
        'Portugal': 'pt.farnell.com',
        'Romania': 'ro.farnell.com',
        'Russia': 'ru.farnell.com',
        'Slovakia': 'sk.farnell.com',
        'Slovenia': 'si.farnell.com',
        'Sweden': 'se.farnell.com',
        'Turkey': 'tr.farnell.com',
    },
    'Newark': {
        'Canada': 'canada.newark.com',
        'Mexico': 'mexico.newark.com',
        'United States': 'www.newark.com',
    },
    'Element14': {
        'China': 'cn.element14.com',
        'Australia': 'au.element14.com',
        'New Zealand': 'nz.element14.com',
        'Hong Kong': 'hk.element14.com',
        'Singapore': 'sg.element14.com',
        'Malaysia': 'my.element14.com',
        'Philippines': 'ph.element14.com',
        'Thailand': 'th.element14.com',
        'India': 'in.element14.com',
        'Taiwan': 'tw.element14.com',
        'Korea': 'kr.element14.com',
        'Vietnam': 'vn.element14.com',
    },
}

SEARCH_HEADERS = [
    'brandName',
    'displayName',
    'sku',
    'translatedManufacturerPartNumber',
    'datasheets',
    'image',
    'attributes',
]

PARAMETERS_MAP = [
    'attributes',
    'attributeLabel',
    'attributeValue',
]

PRICING_MAP = [
    'prices',
    'from',
    'cost',
]

CURRENCIES = {
    STORES['Farnell']['Bulgaria']: 'EUR',
    STORES['Farnell']['Czechia']: 'CZK',
    STORES['Farnell']['Denmark']: 'DKK',
    STORES['Farnell']['Austria']: 'EUR',
    STORES['Farnell']['Switzerland']: 'CHF',
    STORES['Farnell']['Germany']: 'EUR',
    STORES['Farnell']['CPC UK']: 'GBP',
    STORES['Farnell']['CPC Ireland']: 'EUR',
    STORES['Farnell']['Export']: 'GBP',
    STORES['Farnell']['Onecall']: 'GBP',
    STORES['Farnell']['Ireland']: 'EUR',
    STORES['Farnell']['Israel']: 'USD',
    STORES['Farnell']['United Kingdom']: 'GBP',
    STORES['Farnell']['Spain']: 'EUR',
    STORES['Farnell']['Estonia']: 'EUR',
    STORES['Farnell']['Finland']: 'EUR',
    STORES['Farnell']['France']: 'EUR',
    STORES['Farnell']['Hungary']: 'HUF',
    STORES['Farnell']['Italy']: 'EUR',
    STORES['Farnell']['Lithuania']: 'EUR',
    STORES['Farnell']['Latvia']: 'EUR',
    STORES['Farnell']['Belgium']: 'EUR',
    STORES['Farnell']['Netherlands']: 'EUR',
    STORES['Farnell']['Norway']: 'NOK',
    STORES['Farnell']['Poland']: 'PLN',
    STORES['Farnell']['Portugal']: 'EUR',
    STORES['Farnell']['Romania']: 'RON',
    STORES['Farnell']['Russia']: 'EUR',
    STORES['Farnell']['Slovakia']: 'EUR',
    STORES['Farnell']['Slovenia']: 'EUR',
    STORES['Farnell']['Sweden']: 'SEK',
    STORES['Farnell']['Turkey']: 'EUR',
    STORES['Newark']['Canada']: 'CAD',
    STORES['Newark']['Mexico']: 'USD',
    STORES['Newark']['United States']: 'USD',
    STORES['Element14']['China']: 'CNY',
    STORES['Element14']['Australia']: 'AUD',
    STORES['Element14']['New Zealand']: 'NZD',
    STORES['Element14']['Hong Kong']: 'HKD',
    STORES['Element14']['Singapore']: 'SGD',
    STORES['Element14']['Malaysia']: 'MYR',
    STORES['Element14']['Philippines']: 'PHP',
    STORES['Element14']['Thailand']: 'THB',
    STORES['Element14']['India']: 'INR',
    STORES['Element14']['Taiwan']: 'TWD',
    STORES['Element14']['Korea']: 'KRW',
    STORES['Element14']['Vietnam']: 'USD',
}


def get_default_search_keys():
    return [
        'displayName',
        'displayName',
        'revision',
        'keywords',
        'sku',
        'brandName',
        'translatedManufacturerPartNumber',
        'store_url',
        'datasheet_url',
        'image_url',
    ]


def get_default_store_url(supplier: str) -> str:
    ''' Get saved store/location for supplier '''
    import re
    user_settings = config_interface.load_file(settings.CONFIG_ELEMENT14_API)
    default_store = user_settings.get(f'{supplier.upper()}_STORE', '')
    if not default_store:
        from ..common.tools import cprint
        cprint(f'[INFO]\tWarning: Default store "{supplier.upper()}_STORE" value not configured', silent=False)
    url_match = re.match(r'^(.+?) \((.+?)\)$', default_store)
    if url_match:
        return url_match.group(2)
    return STORES[supplier][default_store]


def build_api_url(part_number: str, supplier: str, store_url=None, silent=False) -> str:
    ''' Build API URL based on user settings '''

    user_settings = config_interface.load_file(settings.CONFIG_ELEMENT14_API)
    api_key = user_settings.get('ELEMENT14_PRODUCT_SEARCH_API_KEY', '')
    if not api_key:
        from ..common.tools import cprint
        cprint('[INFO]\tWarning: ELEMENT14_PRODUCT_SEARCH_API_KEY user value not configured', silent=silent)

        import os
        api_key = os.environ.get('ELEMENT14_PART_API_KEY', None)
        if not api_key:
            cprint('[INFO]\tWarning: ELEMENT14_PRODUCT_SEARCH_API_KEY env variable value not found', silent=False)
    if not store_url:
        store_url = get_default_store_url(supplier)

    # Set base URL
    api_url = ELEMENT14_API_URL
    # Set response format
    api_url += '?callInfo.responseDataFormat=JSON'
    # Set result settings: offset = 0; number of results = 1; size = large (eg. to get attributes)
    api_url += '&resultsSettings.offset=0&resultsSettings.numberOfResults=1&resultsSettings.responseGroup=large'
    # Set API key
    api_url += f'&callInfo.apiKey={api_key}'
    # Set store URL
    api_url += f'&storeInfo.id={store_url}'
    # Set part number
    api_url += f'&term=manuPartNum:{part_number}'

    return api_url


def build_image_url(image_data: dict, supplier: str, store_url=None) -> str:
    image_url = 'https://'
    # Set store URL
    if store_url:
        image_url += store_url
    else:
        image_url += get_default_store_url(supplier)
    # Append static text
    image_url += '/productimages/standard'
    # Append locale
    if 'farnell' in image_data['vrntPath']:
        image_url += '/en_GB'
    else:
        image_url += '/en_US'
    # Append image filename
    image_url += image_data['baseName']

    return image_url


def fetch_part_info(part_number: str, supplier: str, store_url=None, silent=False) -> dict:
    ''' Fetch part data from API '''

    part_info = {}

    def search_timeout(timeout=10):
        url = build_api_url(part_number, supplier, store_url, silent)
        response = download(url, timeout=timeout)
        return response

    # Query part number
    try:
        part = search_timeout()
    except:
        part = None

    # Extract result
    try:
        part = part['manufacturerPartNumberSearchReturn'].get('products', [])[0]
    except (TypeError, IndexError):
        part = None

    if not part:
        return part_info

    headers = SEARCH_HEADERS

    for key in part:
        if key in headers:
            if key == 'displayName':
                # String to remove
                str_remove = part['brandName'] + ' - ' + part['translatedManufacturerPartNumber'] + ' - '
                # Remove and limit to 100 chars
                part_info['displayName'] = part['displayName'].replace(str_remove, '')[:100]
            elif key == 'datasheets':
                try:
                    part_info['datasheet_url'] = part['datasheets'][0]['url'].replace('http', 'https')
                except IndexError:
                    pass
            elif key == 'image':
                part_info['image_url'] = build_image_url(part['image'], supplier, store_url)
            elif key == 'attributes':
                part_info['parameters'] = {}
            else:
                part_info[key] = part[key]

    # Parameters
    if 'parameters' in part_info.keys():
        [parameter_key, name_key, value_key] = PARAMETERS_MAP

        try:
            for parameter in range(len(part[parameter_key])):
                parameter_name = part[parameter_key][parameter][name_key]
                parameter_value = part[parameter_key][parameter][value_key]
                # Append to parameters dictionary
                part_info['parameters'][parameter_name] = parameter_value
        except TypeError:
            # Parameter list is empty
            pass

    # Pricing
    part_info['pricing'] = {}
    [pricing_key, qty_key, price_key] = PRICING_MAP

    for price_break in part[pricing_key]:
        quantity = price_break[qty_key]
        price = price_break[price_key]
        part_info['pricing'][quantity] = price
        
    if not store_url:
        store_url = get_default_store_url(supplier)
    part_info['currency'] = CURRENCIES.get(store_url, 'USD')

    # Extra search fields
    if settings.CONFIG_ELEMENT14.get('EXTRA_FIELDS', None):
        for extra_field in settings.CONFIG_ELEMENT14['EXTRA_FIELDS']:
            if part.get(extra_field, None):
                part_info['parameters'][extra_field] = part[extra_field]
            else:
                from ..common.tools import cprint
                cprint(f'[INFO]\tWarning: Extra field "{extra_field}" not found in search results', silent=False)
    
    # Append Store URL
    # Element14 support said "At this time our API is not structured to provide a URL to product pages in the selected storeInfo.id value."
    if store_url:
        part_info['store_url'] = f'https://{store_url}'
    else:
        part_info['store_url'] = f'https://{get_default_store_url(supplier)}'
    # Append search to URL
    part_info['store_url'] += f'/w/search?st={part["translatedManufacturerPartNumber"]}'

    # Append categories
    part_info['category'] = ''
    part_info['subcategory'] = ''

    return part_info


def test_api(store_url=None) -> bool:
    ''' Test method for API '''

    test_success = True

    search_queries = [
        {
            'store_url': 'uk.farnell.com',
            'part_number': '1N4148W-7-F',
            'expected': {
                'displayName': 'DIODE, ULTRAFAST RECOVERY, 300mA, 75V, SOD-123-2, FULL REEL',
                'brandName': 'MULTICOMP PRO',
                'translatedManufacturerPartNumber': '1N4148W-7-F.',
            }
        },
        {
            'store_url': 'www.newark.com',
            'part_number': 'BLM18AG601SN1D',
            'expected': {
                'displayName': 'Ferrite Bead, 0603 [1608 Metric], 600 ohm, 500 mA, EMIFIL BLM18AG Series, 0.38 ohm, ± 25%',
                'brandName': 'MURATA',
                'translatedManufacturerPartNumber': 'BLM18AG601SN1D',
            }
        },
        {
            'store_url': 'au.element14.com',
            'part_number': '2N7002K-T1-GE3',
            'expected': {
                'displayName': 'Power MOSFET, N Channel, 60 V, 190 mA, 2 ohm, SOT-23, Surface Mount',
                'brandName': 'VISHAY',
                'translatedManufacturerPartNumber': '2N7002K-T1-GE3',
            }
        },
    ]

    if store_url:
        # If store URL is specified, only check data is returned (eg. avoid discrepancies between stores)
        part_number = '1N4148'
        test_part = fetch_part_info(part_number, '', store_url, True)
        if not test_part:
            test_success = False
    else:
        for item in search_queries:
            if not test_success:
                break

            test_part = fetch_part_info(item['part_number'], '', item['store_url'], True)

            if not test_part:
                test_success = False
                
            # Check content of response
            if test_success:
                for key, value in item['expected'].items():
                    if test_part[key] != value:
                        print(f'"{test_part[key]}" <> "{value}"')
                        test_success = False
                        break

    return test_success
