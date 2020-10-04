#!/bin/sh
mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"schorfma@uni-bremen.de\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml
