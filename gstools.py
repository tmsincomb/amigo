import gspread
import pandas as pd


class GSTools:
    
    def __init__(self):
        self.gs = gspread.oauth()  # add OAuth2 as ~/.config/gspread/credentials.json; will prop if missing something
        
    def df_from_gs(self, 
                   name: str, 
                   sheet_name: str, 
                   header: list = None, 
                   row_start: int = 0, 
                   row_end: int = None,
                   column_start: int = 0,
                   column_end: int = None,
                   ) -> pd.DataFrame:
        """
        Pandas DataFram from Google Sheet
        Args:
            name (str): Name or Key of the Google Sheet Doc.
            sheet_name (str): Name or Key of the Google Sheet.
            header (list, optional): Column headers for selected rows/columns. Defaults to None which is the first row.
            row_start (int, optional): Index start of row. Defaults to 0.
            row_end (int, optional): Index end of row. Defaults to None.
            column_start (int, optional): Index start of column. Defaults to 0.
            column_end (int, optional): Index end of column. Defaults to None.
        Returns:
            pd.DataFrame: Only 1 df for the specified sheet.
        """
        gs_doc = self.gs.open(name)
        sheet = gs_doc.worksheet(sheet_name)
        rows = sheet.get_all_values()
        # cut ends of rows
        rows = rows[row_start:row_end]
        # cut ends of columns
        rows = [row[column_start:column_end] for row in rows]
        # pull header from first row if not provided
        if not header: 
            header, *body = rows
        else: 
            body = rows
        return  pd.DataFrame(body, columns=header)

    def df_to_gs(self, name: str, sheet_name: str, df: pd.DataFrame) -> None:
        """
        """
        gs_doc = self.gs.open(name)
        tmp = gs_doc.add_worksheet(title='tmp', rows=1, cols=1)
        sheet = gs_doc.worksheet(sheet_name)
        gs_doc.del_worksheet(sheet)
        sheet = gs_doc.add_worksheet(title=sheet_name, rows=1, cols=1)
        gs_doc.del_worksheet(tmp)
        sheet.update([df.columns.values.tolist()] + df.values.tolist())  # simple csv to sheet copy