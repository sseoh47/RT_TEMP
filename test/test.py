
# 서버가 보는 관점
target = "경산시장"
bus = "간선:840"

if bus == "None":
    return {"result": f"{target}로 갈수 있는 버스는 없습니다. 죄송합니다."}

# 버스 찾았을 때 Dict 형태로 반환 데이터 준비
return_data = f"{target}으로 가기 위해 {bus}"
return_data = return_data + "번 버스를 타야합니다. 감사합니다."
    
result = {'root' : 'PATH', "body":return_data}

# 클라이언트 관점


return_data = "경산시장으로 가기 위해 간선:840번 버스를 타야합니다. 감사합니다."
splitlist = return_data.split(' ')

result_data3 = "간선:840번"

result_data3 = ":840"
result_data3 = "840"




