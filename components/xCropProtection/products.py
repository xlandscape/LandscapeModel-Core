import sqlite3
import typing

class ProductDB:
    def __init__(self, db_path: str) -> None:
        self._path = db_path
        self._connection = None
        self._cursor = None
        
    def initialize_db(self):
        try:
            self._connection = sqlite3.connect(self._path)
            self._cursor = self._connection.cursor()
        except sqlite3.Error as error:
            raise RuntimeError(f'Error initializing database: {error}')
    
    @property
    def Path(self) -> typing.Optional[str]:
        return self._path

    @Path.setter
    def Path(self, value: typing.Optional[str]) -> None:
        self._path = value
        
    @property
    def Connection(self) -> typing.Any:
        return self._connection

    @Connection.setter
    def Connection(self, value: typing.Any) -> None:
        self._connection = value

    @property
    def Cursor(self) -> typing.Any:
        return self._path

    @Cursor.setter
    def Cursor(self, value: typing.Any) -> None:
        self._cursor = value

    # Input: list of products, list of application rates
    # Output: a Tuple containing a list of active substances and a list of their application rates retrieved from the product database
    def sample_active_substances(self, products: list[str], product_app_rate: list[float]) -> typing.Tuple[typing.List[str], typing.List[float]]:
        if self._cursor == None:
            self.close_db()
            raise RuntimeError('The database has not been initialized.')
        ais = []
        application_rates = []

        for i in range(0, len(products)):
            product = products[i]
            # Convert product application rate in g/ha to kg/ha (l/ha)
            appl_rate = product_app_rate[i] / 1000

            active_substances = self._cursor.execute("""
                SELECT a.ActiveSubstanceName, f.InclusionLevel_g_per_L
                FROM ActiveSubstances a
                INNER JOIN Formulations as f ON f.ActiveSubstance_ID = a.ActiveSubstance_ID
                INNER JOIN Products as p ON f.Product_ID = p.Product_ID
                WHERE p.ProductName=?
                """, (product,)).fetchall()                                                  
            
            if len(active_substances) > 0:
                # Units of active substances must be g/l of product
                for row in active_substances:
                    # g/ha (application rate of a.s.) = l/ha * g/l
                    as_appl_rate = appl_rate * row[1]
                    ais.append(str(row[0]))
                    application_rates.append(as_appl_rate)
            else:
                ais.append('Unknown active substance')
                application_rates.append(0.0)

        return ais, application_rates

    # Close the database connection
    def close_db(self):
        if self._connection:
            self._connection.close()