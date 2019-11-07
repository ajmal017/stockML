B
    g�]�!  �               @   s�   d dl Z d dlZd dlmZmZmZ d dlZd dlZ	d dlZd dl
mZ d dlmZ d dlmZ d dlZd dlmZ G dd� d�ZdS )�    N)�Session�Request�PreparedRequest)�json_normalize)�datetime)�
monthdeltac               @   s�   e Zd ZdZdZdZdZdZdZdZ	dZ
dd� Zedd� �Zedd� �Zed	d
� �Zedd� �Zedd� �Zedd� �Zdd� Zdd� Zddddddd�fdd�Zdd� Zedd� �ZdS ) �Td� r   c             C   s.   || _ || _|| _|| _|| _|| _|| _d S )N)�access_token�refresh_token�apikey�	client_id�access_token_timestamp�access_token_expires_in�refresh_token_expires_in)�selfr
   r   r   r   r   r   r   � r   �(C:\Users\Umeda\python\stockML\tda_api.py�__init__   s    zTd.__init__c              C   s   d} | S )Nzaccess_token.jsonr   )Z
token_filer   r   r   �get_access_file_name$   s    zTd.get_access_file_namec             C   s   t j| |d�S )N)�unit)�pd�to_datetime)�ts�paramr   r   r   �convert_timestamp_to_time)   s    zTd.convert_timestamp_to_timec          	   C   s&   t |d��}t�| |� W d Q R X d S )N�w)�open�json�dump)�res�f�tFiler   r   r   �dump_json_File.   s    zTd.dump_json_Filec          	   C   s$   t | d��}t�|�}|S Q R X d S )N�r)r   r   �load)r!   r"   �datar   r   r   �load_json_file4   s    
zTd.load_json_filec             C   s8   t �| �}x|�� D ]}|| ||< qW t �|| � d S )N)r   r'   �keysr#   )r!   �paramsr&   �kr   r   r   �update_key_value_in_file;   s    
zTd.update_key_value_in_filec             C   s   t | | �S )N)�int)�dt1�dt2r   r   r   �	diff_timeB   s    zTd.diff_timec             C   sj   t � � }| �|| j�| jkrft�| j| j�}td|� |d | _|| _t	| j|d��}t
�t
�� |� d S )Nzrefreshing tokens tor
   )r
   r   )�timer/   r   r   �tda_authenticater   r   �printr
   �dictr   r+   r   )r   ZcurrTimestampr    r)   r   r   r   �check_access_token_validF   s    

zTd.check_access_token_validc             C   sB   | � �  | j}dd�|�d�}|| jd�}tjd||d�}|�� S )Nz!application/x-www-form-urlencodedz	Bearer {})zContent-Type�Authorization)�symbolr   z1https://api.tdameritrade.com/v1/marketdata/quotes)�headersr)   )r4   r
   �formatr   �requests�getr   )r   r6   r
   r7   r&   �	authReplyr   r   r   �
get_quotesR   s    
zTd.get_quotesN�yearZmonthly�   )�
periodType�	frequency�periodr@   c             C   s�   | � �  | j}dd�| j�d�}|d }|d }|d }	|d }
|||	|
||d�}tjd	| d
 ||d�}|�� }t|�� �}t�|d �}t	�
|d d�|d< |S )Nz!application/x-www-form-urlencodedz	Bearer {})zContent-Typer5   r?   �frequencyTyperA   r@   )r?   rB   rA   r@   �	startDate�endDatez+https://api.tdameritrade.com/v1/marketdata/z/pricehistory)r7   r)   �candlesr   �ms)r4   r
   r8   r9   r:   r   r   r   �	DataFramer   r   )r   r6   rC   rD   �option_paramsr
   r7   r?   rB   rA   r@   r&   r;   rE   �dfr   r   r   �get_price_history^   s$    

zTd.get_price_historyc             C   s�  t d|� |d }t�� }| ��  | j}dd�|�d�}|d | j|d |d d	|d
 d||t|d � dd�
}tj	d||d�}|�
� }t�|d� d}	|d dkr�|d }	|d dkr�|d }	|	�� }
t�� }x�|
D ]�}|	| }|�� }x�|D ]�}t� }t�|| ��� }|�|� |�|� d}xZ|D ]R}|d	k�rJd|d k�rJd	}x.|d D ]"}||�� k�rT|�|| � �qTW �q*W |�r�|�r�q�|jt�|�d	d�}q�W q�W |d |_|S )Nzgetting options, parameters:ZmonthlyOptionz!application/x-www-form-urlencodedz	Bearer {})zContent-Typer5   r6   �contractType�strikeCountT�strike�SZmonthIncrement)
r6   �api_keyrK   rL   ZincludeQuotesrM   �rangeZfromDateZtoDateZ
optionTypez1https://api.tdameritrade.com/v1/marketdata/chains)r7   r)   Zoption_jsonr	   �CALLZcallExpDateMap�PUTZputExpDateMapFZWeekly�descriptionZinterested_columns)�ignore_index)r2   r   �todayr4   r
   r8   �apiKeyr   r9   r:   r   r   r#   r(   r   rG   �list�np�array�flatten�append�Series�columns)r   rH   ZmonthlyOnlyZ
today_date�tokenr7   r&   r;   Z
optionJson�ocZexprDaysrI   �e�vZstrikes�sr$   �valuesZisWeekly�aZ
optionAttrr   r   r   �get_option_chainx   sZ    









zTd.get_option_chainc             C   s(  d}d}g }d}d}d}d}d}	t �|�}|d }d|d  }d}d}
d}d}d}t�|�r�t �|�}|d }|d	 }|d
 }
|d }|d }n|y\t�||| |�}|d }|d	 }tt�� � t�� |d
< t �|t �	� � |d }|d }W n t
k
�r
   td� Y nX t ||||d |
||�}|S )Nzconfig.jsonzaccess_token.jsonr	   ZAPI_KEYzhttps://ZHOSTr   r
   r   r   Z
expires_inr   zcan't open config.json file)r   r'   �path�existsr1   Zauthenticationr2   r0   Zdump_json_filer   �BaseException)�userZsecrete�config_fileZaccess_token_filer&   r
   r   Zredirect_urlZtda_userZtda_passwordr   r   r   r   �tokensr    �tdr   r   r   �init�   sH    



zTd.init)�__name__�
__module__�__qualname__r
   r   rV   r   r6   r   r   r   r   �staticmethodr   r   r#   r'   r+   r/   r4   r<   rJ   re   rm   r   r   r   r   r      s0   2r   )r1   r   r9   r   r   r   �pandasr   �numpyrX   �pandas.io.jsonr   r   �os.pathrf   r0   r   r   r   r   r   r   �<module>   s   