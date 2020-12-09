CREATE TABLE positions(
    entry_time BIGINT,
    ticker_symbol VARCHAR(10),
    entry_price FLOAT,
    units INT,
    exit_time BIGINT,
    exit_price FLOAT,
    PRIMARY KEY (entry_time, ticker_symbol)
);
