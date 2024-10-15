# Refactor the original code from https://github.com/andrey-jef contributed to the Vnstock Legacy project. Reference: https://github.com/thinh-vu/vnstock/blob/legacy/vnstock/funds.py
# Shoutout to andrey_jef for the contribution.

import json
import requests
import pandas as pd
from pandas import json_normalize
from typing import Union, List
from datetime import datetime
from vnstock3.explorer.fmarket.const import _BASE_URL, _FUND_TYPE_MAPPING, _FUND_LIST_COLUMNS, _FUND_LIST_MAPPING
from vnstock3.core.utils.logger import get_logger
from vnstock3.core.utils.user_agent import get_headers

def convert_unix_to_datetime(df_to_convert: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    """Converts all the specified columns of a dataframe to date format and fill NaN for negative values."""
    df = df_to_convert.copy()
    for col in columns:
        df[col] = pd.to_datetime(df[col], unit="ms", utc=True, errors="coerce").dt.strftime("%Y-%m-%d")
        df[col] = df[col].where(df[col].ge("1970-01-01"))
    return df

# MUTUAL FUNDS
class Fund:
    def __init__(self, random_agent:bool=False) -> None:
        """
        Khởi tạo đối tượng để truy cập dữ liệu từ Fmarket.
        """
        self.data_source = "fmarket"
        self.headers = get_headers(data_source=self.data_source, random_agent=random_agent)
        self.base_url = _BASE_URL
        self.fund_list = self.listing()['short_name'].to_list()
        self.details = self.FundDetails(self)

    def listing(self, fund_type:str="") -> pd.DataFrame:
        """
        Truy xuất danh sách tất cả các quỹ mở hiện có trên Fmarket thông qua API. Xem trực tiếp tại https://fmarket.vn

        Tham số:
        ----------
            fund_type (str): Loại quỹ cần lọc. Mặc định là rỗng để lấy tất cả các quỹ. Các loại quỹ hợp lệ bao gồm: 'BALANCED', 'BOND', 'STOCK'
        
        Trả về:
        -------
            pd.DataFrame: DataFrame chứa thông tin của tất cả các quỹ mở hiện có trên Fmarket. 
        """
        fund_type = fund_type.upper()
        fundAssetTypes = _FUND_TYPE_MAPPING.get(fund_type, [])

        if fund_type not in {"", "BALANCED", "BOND", "STOCK"}:
            print(f"Warning: Unsupported fund type: '{fund_type}'. Please choose from: '' to get all funds or specify one of 'BALANCED', 'BOND', or 'STOCK'.")

        # API call
        payload = {
            "types": ["NEW_FUND", "TRADING_FUND"],
            "issuerIds": [],
            "sortOrder": "DESC",
            "sortField": "navTo6Months",
            "page": 1,
            "pageSize": 100,
            "isIpo": False,
            "fundAssetTypes": fundAssetTypes,
            "bondRemainPeriods": [],
            "searchField": "",
            "isBuyByReward": False,
            "thirdAppIds": [],
        }
        url = f"{_BASE_URL}/filter"
        response = requests.post(url, json=payload, headers=self.headers)
        status = response.status_code
        if status == 200:
            data = response.json()
            print("Total number of funds currently listed on Fmarket: ", data["data"]["total"])
            df = json_normalize(data, record_path=["data", "rows"])

            # select columns to display
            df = df[_FUND_LIST_COLUMNS]

            # Convert Unix timestamp to date format
            df = convert_unix_to_datetime(df_to_convert=df, columns=["firstIssueAt", "productNavChange.updateAt"])

            # sort by '36-month NAV change'
            df = df.sort_values(by="productNavChange.navTo36Months", ascending=False)

            # rename column label to snake_case
            df.rename(columns=_FUND_LIST_MAPPING, inplace=True)

            # reset index column
            df = df.reset_index(drop=True)

            return df
        else:
            raise requests.exceptions.HTTPError(f"Error in API response: {response.status_code} - {response.text}")
    class FundDetails:
        def __init__(self, parent):
            self.parent = parent

        def top_holding(self, symbol="SSISCA") -> pd.DataFrame:
            return self._get_fund_details(symbol, 'top_holding')

        def industry_holding(self, symbol="SSISCA") -> pd.DataFrame:
            return self._get_fund_details(symbol, 'industry_holding')

        def nav_report(self, symbol="SSISCA") -> pd.DataFrame:
            return self._get_fund_details(symbol, 'nav_report')

        def asset_holding(self, symbol="SSISCA") -> pd.DataFrame:
            return self._get_fund_details(symbol, 'asset_holding')

        def _get_fund_details(self, symbol, section) -> pd.DataFrame:
            """
            Internal method to retrieve fund details for a specific section.

            Parameters
            ----------
                symbol : str
                    ticker of a fund. A.k.a fund short name
                section : str
                    section of data to retrieve. Options: 'top_holding', 'industry_holding', 'nav_report', 'asset_holding'

            Returns
            -------
                df : pd.DataFrame
                    DataFrame of the current top holdings of the selected fund.
            """

            # validate "symbol" param input
            symbol = symbol.upper()
            if symbol not in self.parent.fund_list:
                print(f"Error: {symbol} is not a valid input.\nCall the listing() method for the list of valid Fund short_name.")
                raise ValueError(f"Invalid symbol: {symbol}")
            try:
                # Lookup a valid "fundID" related to "symbol"
                # invalid symbol exception will be handled in fund_filter()
                fundID = int(self.parent.filter(symbol)["id"][0])
                print(f"Retrieving data for {symbol}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                raise e

            # validate "type" param input
            section_mapping = {
                "top_holding": self.parent.top_holding,
                "industry_holding": self.parent.industry_holding,
                "nav_report": self.parent.nav_report,
                "asset_holding": self.parent.asset_holding,
            }

            if section in section_mapping:
                # Match with appropriate function
                try:
                    df = section_mapping[section](fundId=fundID)
                except KeyError as e:
                    print(f"Error: Missing expected columns in the response data - {str(e)}")
                    raise ValueError(f"Missing expected columns in the response data - {str(e)}")
                df["short_name"] = symbol
                return df
            else:
                print(f"Error: {section} is not a valid input.\n4 current options are:\ntop_holding\nindustry_holding\nnav_report\nasset_holding")
                raise ValueError

    def filter(self, symbol:str="") -> pd.DataFrame:
        """
        Truy xuất danh sách quỹ theo tên viết tắt (short_name) và mã id của quỹ. Mặc định là rỗng để liệt kê tất cả các quỹ.

        Tham số:
        ----------
            symbol (str): Tên viết tắt của quỹ cần tìm kiếm. Mặc định là rỗng để lấy tất cả các quỹ.

        Trả về:
        -------
            pd.DataFrame: DataFrame chứa thông tin của quỹ cần tìm kiếm.
        """

        symbol = symbol.upper()

        payload = {
            "searchField": symbol,
            "types": ["NEW_FUND", "TRADING_FUND"],
            "pageSize": 100,
        }
        url = f"{_BASE_URL}/filter"
        payload = json.dumps(payload)
        response = requests.post(url, data=payload, headers=self.headers)

        if response.status_code == 200:
            data = response.json()
            df = json_normalize(data, record_path=["data", "rows"])
            if not df.empty:
                # retrieve only column_subset
                column_subset = ["id", "shortName"]
                df = df[column_subset]
                return df
            else:
                raise ValueError(f"No fund found with this symbol {symbol}.\nSee funds_listing() for the list of valid Fund short names.")
        else:
            raise requests.exceptions.HTTPError(f"Error in API response: {response.status_code} - {response.text}")

    def top_holding(self, fundId:int=23) -> pd.DataFrame:
        """
        Retrieve list of top 10 holdings in the specified fund. Live data is retrieved from the Fmarket API.

        Parameters
        ----------
            fundId : int
                id of a fund in fmarket database
        Returns
        -------
            df : pd.DataFrame
                DataFrame of the current top 10 holdings of the selected fund.
        """

        # API call
        # Logic: there are funds which allocate to either equities or fixed income securities, or both
        url = f"{_BASE_URL}/{fundId}"
        response = requests.get(url, headers=self.headers, cookies=None)
        status = response.status_code
        if status == 200:
            data = response.json()
            df = pd.DataFrame()

            # Flatten top holding equities
            df_stock = json_normalize(data, record_path=["data", "productTopHoldingList"])
            if not df_stock.empty:
                # Convert unix timestamp into date format
                df_stock = convert_unix_to_datetime(df_to_convert=df_stock, columns=["updateAt"])
                # Merge to output
                df = pd.concat([df, df_stock])

            # Flatten top holding fixed income securities
            df_bond = json_normalize(data, record_path=["data", "productTopHoldingBondList"])
            if not df_bond.empty:
                df_bond = convert_unix_to_datetime(df_to_convert=df_bond, columns=["updateAt"])
                df = pd.concat([df, df_bond])

            # if df is not empty, then rearrange and return df as output
            if not df.empty:
                df["fundId"] = int(fundId)
                # rearrange columns to display
                column_subset = [
                    "stockCode",
                    "industry",
                    "netAssetPercent",
                    "type",
                    "updateAt",
                    "fundId",
                ]

                existing_columns = [col for col in column_subset if col in df.columns]
                df = df[existing_columns]

                # rename column label to snake_case
                column_mapping = {
                    "stockCode": "stock_code",
                    "industry": "industry",
                    "netAssetPercent": "net_asset_percent",
                    "type": "type_asset",
                    "updateAt": "update_at",
                }
                # Only rename columns that exist in the DataFrame
                existing_column_mapping = {k: v if k in df.columns else k for k, v in column_mapping.items()}
                df.rename(columns=existing_column_mapping, inplace=True)

                return df
            else:
                print(f"Warning: No data available for fundId {fundId}.")
                return pd.DataFrame()
        else:
            # invalid fundId error is 400 from api
            raise requests.exceptions.HTTPError(f"Error in API response: {response.status_code} - {response.text}")

    def industry_holding(self, fundId:int=23) -> pd.DataFrame:
        """Retrieve list of industries and fund distribution for specific fundID. Live data is retrieved from the Fmarket API.

        Parameters
        ----------
            fundId : int
                id of a fund in fmarket database

        Returns
        -------
            df : pd.DataFrame
                DataFrame of the current top industries in the selected fund.
        """

        # API call
        url = f"{_BASE_URL}/{fundId}"
        response = requests.get(url, headers=self.headers, cookies=None)

        if response.status_code == 200:
            data = response.json()
            df = json_normalize(data, record_path=["data", "productIndustriesHoldingList"])

            # rearrange columns to display
            column_subset = [
                "industry",
                "assetPercent",
            ]

            existing_columns = [col for col in column_subset if col in df.columns]
            df = df[existing_columns]

            # rename column label to snake_case
            column_mapping = {
                "industry": "industry",
                "assetPercent": "net_asset_percent",
            }

            # Only rename columns that exist in the DataFrame
            existing_column_mapping = {k: v if k in df.columns else k for k, v in column_mapping.items()}
            df.rename(columns=existing_column_mapping, inplace=True)

            return df
        else:
            # invalid fundId error is 400 from api
            raise requests.exceptions.HTTPError(f"Error in API response: {response.status_code} - {response.text}")

    def nav_report(self, fundId:int=23) -> pd.DataFrame:
        """Retrieve all available daily NAV data point of the specified fund. Live data is retrieved from the Fmarket API.

        Parameters
        ----------
            fundId : int
                id of a fund in fmarket database.

        Returns
        -------
            df : pd.DataFrame
                DataFrame of all avalaible daily NAV data points of the selected fund.
        """

        # API call
        # Set the date range to the current date
        current_date = datetime.now().strftime("%Y%m%d")
        url = f"{_BASE_URL[:-1]}/get-nav-history"
        payload = {
            "isAllData": 1,
            "productId": fundId,
            "fromDate": None,
            "toDate": current_date,
        }
        response = requests.post(url, json=payload)
        status = response.status_code
        if status == 200:
            data = response.json()
            df = json_normalize(data, record_path=["data"])

            if not df.empty:
                # rearrange columns to display
                column_subset = ["navDate", "nav"]

                existing_columns = [col for col in column_subset if col in df.columns]
                df = df[existing_columns]

                # rename column label to snake_case
                column_mapping = {
                    "navDate": "date",
                    "nav": "nav_per_unit",
                }

                # Only rename columns that exist in the DataFrame
                existing_column_mapping = {k: v if k in df.columns else k for k, v in column_mapping.items()}
                df.rename(columns=existing_column_mapping, inplace=True)

                return df
            else:
                raise ValueError(f"No data with this fund_id {fundId}")
        else:
            raise requests.exceptions.HTTPError(f"Error in API response: {response.status_code} - {response.text}")

    def asset_holding(self, fundId:int=23) -> pd.DataFrame:
        """Retrieve list of assets holding allocation for specific fundID. Live data is retrieved from the Fmarket API.

        Parameters
        ----------
            fundId : int
                id of a fund in fmarket database.

        Returns
        -------
            df : pd.DataFrame
                DataFrame of assets holding allocation of the selected fund.
        """

        # API call
        url = f"{_BASE_URL}/{fundId}"
        response = requests.get(url, headers=self.headers, cookies=None)
        if response.status_code == 200:
            data = response.json()
            df = json_normalize(data, record_path=["data", "productAssetHoldingList"])

            # rearrange columns to display
            column_subset = [
                "assetPercent",
                "assetType.name",
            ]

            existing_columns = [col for col in column_subset if col in df.columns]
            df = df[existing_columns]

            # rename column label to snake_case
            column_mapping = {
                "assetPercent": "asset_percent",
                "assetType.name": "asset_type",
            }

            # Only rename columns that exist in the DataFrame
            existing_column_mapping = {k: v if k in df.columns else k for k, v in column_mapping.items()}
            df.rename(columns=existing_column_mapping, inplace=True)

            return df
        else:
            # invalid fundId error is 400 from api
            raise requests.exceptions.HTTPError(f"Error in API response: {response.status_code} - {response.text}")