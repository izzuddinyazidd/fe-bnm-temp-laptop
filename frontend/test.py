def read_sharepoint_file(

    url: str,

    file_as: Literal["workbook", "dataframe", "raw"] = "dataframe",

    sheet_index_col: int | Sequence[int] | str | None = 0,

):

    """

    Read Excel files from DSA/DARE's SharePoint using 3 potential modes via `file_as`:

        - "workbook": reads using openpyxl

        - "dataframe": reads using Pandas DataFrame

        - "raw": returns a BytesIO bytes file object, useful if you wanna use a custom file reader or read a non-Excel file



    :url `str`: the SharePoint URL to a file e.g. `https://banknegaramy.sharepoint.com/:x:/r/sites/DSA/Shared%20Documents/Projects/DARE%20-%20DAREBoard%20aka%20Real%20Time%20Economics%20Dashboard/Dashboard%20Data/03%20Infokit_interest%20rates.xlsx`\n

    :file_as `Literal["workbook", "dict[str, DataFrame]", "raw"]`: file read modes

    :sheet_index_col `int | Sequence[int] | str | None`: default is col 0. If you don't want to have an index column, set to None.

    """

    parsed_url = urlparse(url)

    hostname = parsed_url.hostname

    path_parts = parsed_url.path.split("/")

    site_name = path_parts[4]



    # get the site id

    site_id = get_sharepoint_id(f"sites/{hostname}:/sites/{site_name}")



    # get the drive id

    drive_id = get_sharepoint_id(f"sites/{site_id}/drive")



    # get the item id

    item_url = "/".join(path_parts[6:])

    item_id = get_sharepoint_id(f"drives/{drive_id}/root:/{item_url}")



    result = call_sharepoint_api_raw(f"/sites/{site_id}/drive/items/{item_id}/content")



    bytes_file_obj = io.BytesIO()

    bytes_file_obj.write(result.content)

    bytes_file_obj.seek(0)  # set file object to start



    if file_as == "workbook":

        return load_workbook(bytes_file_obj, data_only=True)

    elif file_as == "dataframe":

        df = pd.read_excel(bytes_file_obj, sheet_name=None, index_col=sheet_index_col)

        return df

    else:

        return bytes_file_obj





@retry_func

def get_sharepoint_token() -> str:

    """

    Returns the SharePoint / MS Graph API access_token string

    """

    URL = "https://login.microsoftonline.com/aac700cd-c721-4651-98dd-b78544c94fd6/oauth2/v2.0/token"



    response = requests.post(

        URL,

        data={

            "client_id": os.getenv("MS_GRAPH_API_CLIENT_ID", ""),

            "client_secret": os.getenv("MS_GRAPH_API_CLIENT_SECRET", ""),

            "scope": "https://graph.microsoft.com/.default",

            "grant_type": "client_credentials",

        },

    )



    if response.status_code == 400:

        raise ValueError(response.text)

    else:

        access_token = json.loads(response.text)["access_token"]



    return access_token





def call_sharepoint_api_raw(url: str) -> requests.Response:

    """

    Returns raw SharePoint / MS Graph API response

    """

    access_token = get_sharepoint_token()



    response = fetch(

        "https://graph.microsoft.com/v1.0/" + url,

        headers={"Authorization": "Bearer " + access_token},

    )



    if response.status_code == 200:

        return response

    else:

        raise ValueError(response.text)





def call_sharepoint_api(url: str) -> dict:

    """

    Returns info of a SharePoint site/drive/folder based on the URL

    """



    response = call_sharepoint_api_raw(url=url)

    response_dict = json.loads(response.text)

    return response_dict





def get_sharepoint_id(url: str) -> str:

    df = pd.read_csv(f"{PROJECT_ROOT_DIR}/raw-data/sharepoint_ids.csv")



    def get_id_or_none() -> str | None:

        """

        Check if ID is already stored in CSV

        """

        match = df[df["url"] == url]

        if match.empty is False:

            return match["id"].iloc[0]

        return None



    id = get_id_or_none()



    # If ID is not found in CSV, call the SharePoint API to retrieve the ID

    if id is None:

        data = call_sharepoint_api(url=url)

        id = data["id"]



        # Memoize the ID in CSV

        df = pd.concat(

            [df, pd.DataFrame({"url": [url], "id": [id]})], ignore_index=True

        )

        df.to_csv(f"{PROJECT_ROOT_DIR}/raw-data/sharepoint_ids.csv", index=False)



    return id





def upload_sharepoint(

    hostname: str, site_name: str, folder_path: str, filename: str

) -> requests.Response:

    """

    Upload files to a SharePoint folder.

    """

    # get the site id

    site_id = get_sharepoint_id(f"sites/{hostname}:/sites/{site_name}")



    # get the drive id

    drive_id = get_sharepoint_id(f"sites/{site_id}/drive")



    access_token = get_sharepoint_token()



    file_path = f"{PROJECT_ROOT_DIR}/{BUCKET_NAME_CATALOGUE}/{filename}"



    with open(file_path, "rb") as file:

        print("Uploading to Sharepoint...")

        upload_url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drives/{drive_id}/items/root:/{folder_path}/{filename}:/content"

        headers = {

            "Authorization": "Bearer " + access_token,

            "Content-Type": "application/octet-strem",

            "Content-Length": str(os.path.getsize(file_path)),

        }

        response = requests.put(upload_url, headers=headers, data=file)

        return response