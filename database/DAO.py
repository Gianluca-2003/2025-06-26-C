from database.DB_connect import DBConnect
from model.constructors import Constructor


class DAO():
    @staticmethod
    def getAllConstructors():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """SELECT * 
                    from constructors"""
        cursor.execute(query)

        res = []
        for row in cursor:
            res.append(row)

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def get_nodes():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select c.*
                from constructors c """
        cursor.execute(query)

        res = []
        for row in cursor:
            res.append(Constructor(**row))

        cursor.close()
        cnx.close()
        return res


    @staticmethod
    def get_edges(y_min,y_max,idMap):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select distinct t1.constructorId as n1, t2.constructorId as n2
               from (select c.constructorId
                from constructors c , races r ,results re
                where c.constructorId = re.constructorId
                and re.raceId = r.raceId
                and r.`year` >= %s
                and r.`year` <= %s
                group by c.constructorId
                having count(*) >=1) t1,
                (select c.constructorId
                from constructors c , races r ,results re
                where c.constructorId = re.constructorId
                and re.raceId = r.raceId
                and r.`year` >= %s
                and r.`year` <= %s
                group by c.constructorId
                having count(*) >=1) t2,
                results re1, results re2
        where t1.constructorId = re1.constructorId
        and t2.constructorId = re2.constructorId
        and re1.`position` is not null
        and re2.`position` is not null
        and t1.constructorId < t2.constructorId"""

        cursor.execute(query,(y_min,y_max,y_min,y_max,))

        res = []
        for row in cursor:
            res.append((idMap[row['n1']],idMap[row['n2']]))

        cursor.close()
        cnx.close()
        return res


    @staticmethod
    def get_pesi(y_min,y_max):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select t1.constructorId as id, count( r.raceId) as peso
                from (select c.constructorId
                    from constructors c , races r ,results re
                    where c.constructorId = re.constructorId
                    and re.raceId = r.raceId
                    and r.`year` >= %s
                    and r.`year` <= %s
                    group by c.constructorId
                    having count(*) >=1) t1,
                    results r, races r2 
                where t1.constructorId = r.constructorId
                and r.`position` is not null
                and r2.raceId = r.raceId
                and r2.`year` >= %s
                and r2.`year` <= %s
                group by t1.constructorId"""
        cursor.execute(query,(y_min,y_max,y_min,y_max,))

        res = {}
        for row in cursor:
            res[row['id']] = row['peso']

        cursor.close()
        cnx.close()
        return res


    @staticmethod
    def get_pesi_totoli(y_min,y_max):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select t1.constructorId as id, count( r.raceId) as peso
                from (select c.constructorId
                    from constructors c , races r ,results re
                    where c.constructorId = re.constructorId
                    and re.raceId = r.raceId
                    and r.`year` >= %s
                    and r.`year` <= %s
                    group by c.constructorId
                    having count(*) >=1) t1,
                    results r, races r2 
                where t1.constructorId = r.constructorId
                and r2.raceId = r.raceId
                and r2.`year` >= %s
                and r2.`year` <= %s
                group by t1.constructorId"""
        cursor.execute(query,(y_min,y_max,y_min,y_max,))

        res = {}
        for row in cursor:
            res[row['id']] = row['peso']

        cursor.close()
        cnx.close()
        return res


    @staticmethod
    def get_validi_costuttori(y_min,y_max,m,idMap):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select c.constructorId as id, count(distinct r.`year`) as campionati
                from constructors c,races r , results re
                where r.raceId = re.raceId
                and c.constructorId = re.constructorId
                and r.year >= %s
                and r.`year` <= %s
                group by c.constructorId
                having campionati >= %s"""
        cursor.execute(query,(y_min,y_max,m,))

        res = []
        for row in cursor:
                   res.append(idMap[row['id']])

        cursor.close()
        cnx.close()
        return res



    @staticmethod
    def get_years():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select distinct r.`year` as year
                    from races r 
                    order by r.`year` desc"""
        cursor.execute(query)

        res = []
        for row in cursor:
            res.append(row['year'])

        cursor.close()
        cnx.close()
        return res







