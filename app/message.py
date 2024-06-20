msg = {}
msg[20000] = {"descriptionEn": 'Success', "description": 'ทำรายการเรียบร้อย' }
msg[20001] = {"descriptionEn": 'Cannot register Mobile No. is duplicate', "description": 'ผู้ใช้งานนี้มีอยู่ในระบบแล้ว' }
msg[20004] = {"descriptionEn": 'Please wait admin approve', "description": 'ข้อมูลร้านค้าอยู่ระหว่างการอนุมัติ' }

msg[40000] = {"descriptionEn": 'Bad Request', "description": 'การร้องขอไม่ถูกต้อง' }
msg[40100] = {"descriptionEn": 'Unauthorized Key', "description": 'รหัสผ่านการเข้าไม่ถูกต้อง' }
msg[40102] = {"descriptionEn": 'Token not match or Token expired', "description": 'รหัสผ่านไม่ตรงกันหรือ รหัสผ่านหมดอายุ'}
msg[40103] = {"descriptionEn": 'API not allow for user', "description": 'API นี้ไม่อณุญาติให้ใช้งาน'}
msg[40104] = {"descriptionEn": 'Invalid username or password', "description": 'ชื่อผู้ใช้งานหรือรหัสผ่านไม่ถูกต้อง' }
msg[40105] = {"descriptionEn": 'Invalid password', "description": 'รหัสผ่านไม่ถูกต้อง' }
msg[40106] = {"descriptionEn": 'Please authentication with one time password', "description": 'รหัสยืนยันไม่ถูกต้อง' }
msg[40107] = {"descriptionEn": 'Please verify "code"', "description": 'กรุณายืนยันตัวตนให้เรียบร้อย' }
msg[40108] = {"descriptionEn": 'Please verify "code" Token not expired ', "description": 'กรุณายืนยันตัวตนให้เรียบร้อย รหัสผ่านยังไม่หมดอายุ' }
msg[40300] = {"descriptionEn": 'Missing or invalid parameter', "description": 'ข้อมูลไม่ครบ หรือข้อมูลผิดพลาด' }
msg[40301] = {"descriptionEn": 'Data is duplicated', "description": 'มีข้อมูลนี้อยู่แล้ว' }
msg[40307] = {"descriptionEn": 'Please your check zMP Wallet', "description": 'กรุณาตรวจสอบยอกคงเหลือ zMP' }
msg[40400] = {"descriptionEn": 'Unknow URL', "description": 'ไม่รู้จัก URL นี้' }
msg[40401] = {"descriptionEn": 'Data Not Found', "description": 'ไม่พบข้อมูลที่ต้องการ' }
msg[40402] = {"descriptionEn": 'User Not Found', "description": 'ไม่พบผู้ใช้งานในระบบ' }

msg[50000] = {"descriptionEn": 'System Error', "description": 'ระบบมีปัญหา' }
msg[50001] = {"descriptionEn": 'Mongodb connection error', "description": 'การเชื่อมต่อฐานข้อมูลมีปัญหา' }
msg[50002] = {"descriptionEn": 'Mongodb query error', "description": 'การค้นหาข้อมูลจากฐานข้อมูลมีปัญหา' }
msg[50003] = {"descriptionEn": 'Mongodb insert error', "description": 'การบันทึกข้อมูลลงฐานข้อมูลมีปัญหา' }
msg[50004] = {"descriptionEn": 'Mongodb update error', "description": 'การแก้ไขข้อมูลมีปัญหา' }
msg[50005] = {"descriptionEn": 'Mongodb delete error', "description": 'การลบข้อมูลมีปัญหา' }
msg[50006] = {"descriptionEn": 'Send SMS error!', "description": 'ไม่สามารถส่ง SMS ได้' }
msg[70001] = {"descriptionEn": 'Create token error', "description": 'ไม่สามารถสร้างรหัสผ่านได้' }
msg[80000] = {"descriptionEn": 'Invalid credencial', "description": 'ไม่สามารถ อัปเกรดกระเป๋าเงินได้' }

def getMsg(code):
    return msg[code]
    