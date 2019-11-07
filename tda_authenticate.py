B
    8��]  �               @   s�   d dl Z d dlZ d dlZd dlZd dlZd dlmZ d dlmZ d dl	m
Z d dlZddd�Zdd� Zdd	� Zed
kr|e�  dS )�    N)�	webdriver)�whichc          
   C   s  | d } t d| � dt�|� d t�| � }t�� }tjdkrhtj�	d�rTd|_
q�tj�	d�r�d|_
nLdtjkr�td	�p�td
�p�td�|_
n&tj�	d�r�d|_
ntj�	d�r�d|_
td�p�d}tj||d�}t d|� |�|� |p�tj�dd�}|�ptj�dd�}|�r�|�r�|�d�}|�d�}	|�|� |	�|� |�d���  |�d���  xty2t�|j�d�d �}
|
dk�r�P n
t�d� W n ttfk
�r�   Y nX �qZW ntd� t�|j�d�d �}
|��  tjdddiddd |
| |d!�d"�}|jd#k�rtd$��|�� S )%Nz@AMER.OAUTHAPz
client_id:zChttps://auth.tdameritrade.com/auth?response_type=code&redirect_uri=z&client_id=�darwinz</Applications/Google Chrome.app/Contents/MacOS/Google Chromez5/Applications/Chrome.app/Contents/MacOS/Google ChromeZlinuxzgoogle-chromeZchromeZchromiumz;C:/Program Files (x86)/Google/Chrome/Application/chrome.exez5C:/Program Files/Google/Chrome/Application/chrome.exeZchromedriverz/usr/local/bin/chromedriver)Zchrome_optionszfound driverZTDAUSER� ZTDAPASSZusernameZpasswordZacceptzcode=�   �   z*after giving access, hit enter to continuez,https://api.tdameritrade.com/v1/oauth2/tokenzContent-Typez!application/x-www-form-urlencodedZauthorization_codeZoffline)�
grant_type�refresh_tokenZaccess_type�code�	client_id�redirect_uri)�headers�data��   zCould not authenticate!) �print�up�quoter   ZChromeOptions�sys�platform�os�path�existsZbinary_locationr   ZChrome�get�environZfind_element_by_idZ	send_keysZclickZunquoteZcurrent_url�split�timeZsleep�	TypeError�
IndexError�input�close�requests�post�status_code�	Exception�json)r   r   ZtdauserZtdapassZurlZoptionsZchrome_driver_binaryZdriverZuboxZpboxr
   �resp� r&   �1C:\Users\Umeda\python\stockML\tda_authenticate.py�authentication   sd    









r(   c             C   s6   t jdddid| |d�d�}|jdkr.td��|�� S )	Nz,https://api.tdameritrade.com/v1/oauth2/tokenzContent-Typez!application/x-www-form-urlencodedr	   )r   r	   r   )r   r   r   zCould not authenticate!)r    r!   r"   r#   r$   )r	   r   r%   r&   r&   r'   r	   Q   s    
r	   c           	   C   sn   d} g }y"t | ��}t�|�}W d Q R X W n tk
rF   td� Y nX |d }d|d  }tt||�� d S )Nzconfig.jsonzcan't open config.json file�API_KEYzhttps://�HOST)�openr$   �load�BaseExceptionr   r(   )�config_filer   �	json_filer   �redirect_urlr&   r&   r'   �main\   s    
r1   �__main__)NN)r   Zos.pathr   r    r   Zseleniumr   Zshutilr   Zurllib.parseZparser   r$   r(   r	   r1   �__name__r&   r&   r&   r'   �<module>   s   
F