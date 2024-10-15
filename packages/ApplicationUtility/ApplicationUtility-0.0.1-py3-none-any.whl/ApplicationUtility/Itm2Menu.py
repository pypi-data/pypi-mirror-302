from itertools import islice
import cx_Oracle
from datetime import datetime
import loggerutility as logger


class Itm2Menu:

    data = {}
    
    def check_and_insert_delete_itm2menu_table(self, navigation,conn):
        if not conn:
            raise Exception("Oracle connection is not established.")
        
        # logger.log(f"navigation:;  {navigation}")
        for navigations in navigation:
            logger.log(f"navigations::  {navigations}")
        
            cursor = conn.cursor()

            required_keys = ['id','level_1','level_2','level_3','level_4','level_5']
            missing_keys = [key for key in required_keys if key not in navigations]
            logger.log(f"Missing required keys for ITM2MENU table: {', '.join(missing_keys)}")

            if missing_keys:
                raise KeyError(f"Missing required keys for ITM2MENU table: {', '.join(missing_keys)}")
            else:
                application = navigations.get('id', '')[:3]
                logger.log(f"app_name:;  {application}")
                level_1 = navigations.get('level_1', 0)
                level_2 = navigations.get('level_2', 0)
                level_3 = navigations.get('level_3', 0)
                level_4 = navigations.get('level_4', 0)
                level_5 = navigations.get('level_5', 0)
                win_name = navigations.get('obj_name', '')
                descr = navigations.get('description', '')[:40]
                comments = navigations.get('comments', '')
                menu_path = navigations.get('menu_path', '')
                icon_path = navigations.get('icon_path', '')
                close_icon = navigations.get('close_icon', '')
                open_icon = navigations.get('open_icon', '')
                obj_type = navigations.get('obj_type', '')
                chg_date = datetime.now().strftime('%d-%m-%y')
                chg_term = navigations.get('chg_term', '').strip() or 'System'
                chg_user = navigations.get('chg_user', '').strip() or 'System'
                mob_deploy = navigations.get('mob_deploy', '')
                default_state = navigations.get('default_state', '')
                def_action = navigations.get('def_action', '')
                mob_deply = navigations.get('mob_deply', '')
                ent_types = navigations.get('ent_types', '')

            
                # Prepare the WHERE clause for checking if row exists
                where_clause = """APPLICATION = :APPLICATION AND 
                    LEVEL_1 = :LEVEL_1 AND 
                    LEVEL_2 = :LEVEL_2 AND 
                    LEVEL_3 = :LEVEL_3 AND 
                    LEVEL_4 = :LEVEL_4 AND 
                    LEVEL_5 = :LEVEL_5"""
                
                # Check if row exists
                select_query = f"SELECT COUNT(*) FROM ITM2MENU WHERE {where_clause}"
                cursor.execute(select_query, {
                    "APPLICATION":application,
                    "LEVEL_1":level_1,
                    "LEVEL_2":level_2,
                    "LEVEL_3":level_3,
                    "LEVEL_4":level_4,
                    "LEVEL_5":level_5
                })
                row_exists = cursor.fetchone()[0]
                logger.log(f"row_exists   {row_exists}")
                if row_exists:
                    logger.log("inside delete")
                    delete_query = f"DELETE FROM ITM2MENU WHERE {where_clause}"
                    cursor.execute(delete_query, {
                        "APPLICATION":application,
                        "LEVEL_1":level_1,
                        "LEVEL_2":level_2,
                        "LEVEL_3":level_3,
                        "LEVEL_4":level_4,
                        "LEVEL_5":level_5
                    })
                    logger.log("Data deleted")

                insert_query = """INSERT INTO ITM2MENU (APPLICATION, LEVEL_1, LEVEL_2, LEVEL_3, LEVEL_4, LEVEL_5, WIN_NAME, DESCR, COMMENTS, 
                    MENU_PATH, ICON_PATH, CLOSE_ICON, OPEN_ICON, OBJ_TYPE, CHG_DATE, CHG_TERM, CHG_USER, 
                    MOB_DEPLOY, DEFAULT_STATE, DEF_ACTION, MOB_DEPLY, ENT_TYPES) 
                    VALUES (:APPLICATION, :LEVEL_1, :LEVEL_2, :LEVEL_3, :LEVEL_4, :LEVEL_5, :WIN_NAME, :DESCR, 
                    :COMMENTS, :MENU_PATH, :ICON_PATH, :CLOSE_ICON, :OPEN_ICON, :OBJ_TYPE, 
                    TO_DATE(:CHG_DATE, 'DD-MM-YY'), :CHG_TERM, :CHG_USER, :MOB_DEPLOY, :DEFAULT_STATE, 
                    :DEF_ACTION, :MOB_DEPLY, :ENT_TYPES)"""
                
                cursor.execute(insert_query,{
                    'application': application,
                    'level_1': level_1,
                    'level_2': level_2,
                    'level_3': level_3,
                    'level_4': level_4,
                    'level_5': level_5,
                    'win_name': win_name,
                    'descr': descr,
                    'comments': comments,
                    'menu_path': menu_path,
                    'icon_path': icon_path,
                    'close_icon': close_icon,
                    'open_icon': open_icon,
                    'obj_type': obj_type,
                    'chg_date': chg_date,
                    'chg_term': chg_term,
                    'chg_user': chg_user,
                    'mob_deploy': mob_deploy,
                    'default_state': default_state,
                    'def_action': def_action,
                    'mob_deply': mob_deply,
                    'ent_types': ent_types
                })
                logger.log(f"Data inserted")

    def process_data(self, conn, menu_model):
        # self.sql_models = menu_model
        if "navigation" in menu_model:
            navigation = menu_model["navigation"]
            # logger.log(f"navigation:::  {navigation}")
            self.check_and_insert_delete_itm2menu_table(navigation, conn)
            

