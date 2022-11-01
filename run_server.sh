#!/bin/bash

source C:/Users/asus/.venv/web/Scripts/activate;
export API_KEY=$(cat apikey);
python app.py
