import requests
from bs4 import BeautifulSoup
from elDNIModule import requisitos

def consultaDni(dni):
    try:
        token, cookies = requisitos()
        headers = {
            'Cache-Control': 'max-age=0',
            'Sec-Ch-Ua': '"Chromium";v="129", "Not=A?Brand";v="8"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Accept-Language': 'es-ES,es;q=0.9',
            'Origin': 'https://eldni.com',
            'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryeiJcT26KdWtoT2Bb',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.6668.71 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'Referer': 'https://eldni.com/',
            'Accept-Encoding': 'gzip, deflate, br',
            'Priority': 'u=0, i',
            'Cookie': str(cookies)
        }

        data = '\r\n------WebKitFormBoundaryeiJcT26KdWtoT2Bb\r\nContent-Disposition: form-data; name="_token"\r\n\r\n'+str(token)+'\r\n------WebKitFormBoundaryeiJcT26KdWtoT2Bb\r\nContent-Disposition: form-data; name="dni"\r\n\r\n'+str(dni)+'\r\n------WebKitFormBoundaryeiJcT26KdWtoT2Bb--'

        t = requests.post('https://eldni.com/pe/buscar-datos-por-dni',data=data,headers=headers)

        soup = BeautifulSoup(t.text,'html.parser')
        nombre = soup.find(id='nombres')['value']
        apellidop = soup.find(id='apellidop')['value']
        apellidom = soup.find(id='apellidom')['value']
        completos = soup.find(id='completos')['value']

        d = {
            'Status':True,
            'datos':{
                'Nombre':nombre,
                'ApellidoP':apellidop,
                'ApellidoM':apellidom,
                'NombreCompleto':completos,
                'Fuente':'https://eldni.com/'
            }
        }

        return d
    except:
        d = {
            'Status':False,
            'datos':{
                
            }
        }
        return d



