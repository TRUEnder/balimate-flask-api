from mysql.connector import pooling

dbConfig = {
    "host": "34.101.200.213",
    "user": "root",
    "password": "balimate",
    "database": "balimate"
}

pool = pooling.MySQLConnectionPool(pool_name='my_pool',
                                   pool_size=3,
                                   **dbConfig)
