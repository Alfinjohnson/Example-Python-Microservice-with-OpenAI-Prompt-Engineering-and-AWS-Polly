-- create topic back service

curl --location 'http://127.0.0.1:8044/createTopic' \
--header 'Content-Type: application/json' \
--data '{
    "title": "msi world",
    "description": "MSI is a product quality of technology.For more product information, please go to https://www.msi.com",
    "chapter_name": " msi"
}'


-- add reference 

curl --location --request PUT 'http://127.0.0.1:8044/addReference' \
--header 'Content-Type: application/json' \
--data '{
    "topic_id": "msiworldchappptestvdd",
    "type": "image",
    "link": "http://google.co/vidwo/214234",
    "description": "hello to this new course",
    "title": "msi",
    "chapter_name": "msi",
    "start_time": 4.21
}'

notes: title -- current word