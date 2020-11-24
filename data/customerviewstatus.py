from appsettings import Settings
from .connection import Connection
import pyodbc
import copy
import arrow


class CustomerViewStatus:

    def __init__(self, ):
        self.data = []
        self.settings = Settings()
        self.generate_data()
        self.load_data()
        return

    def generate_data(self):
        conn = pyodbc.connect(Connection().value())
        cursor = conn.cursor()
        cmd = """
            /*
                Determine who has viewed online e-docs, 
                and hopefully viewed their most recent statement.
            */
            declare @statement_maildate datetime;
            declare @statement_id int = 0;
    
            /* Determine the last statement maildate */
            select top 1 
                @statement_maildate = bs.maildate,
                @statement_id = Statement_ID 
            from BillStatement bs
            where bs.printed = 1
            order by bs.Statement_ID desc;
    
            select x.Name_ID, x.AmtDue as Balance into #Balances from xBegBal x where x.Statement_ID = @statement_id;
    
            select distinct l.name_id into #viewed_statement from WebAccessLog l
            join name n on l.Name_ID = n.NAME_ID
            where l.WebUserLoginID > 999 and l.Logmsg like '%/Edocs/%' and l.AccessDate > ( @statement_maildate - 1 )
    
            select distinct l.name_id into #viewed_internally from WebAccessLog l
            join name n on l.Name_ID = n.NAME_ID
            where l.WebUserLoginID < 1000 and l.Logmsg like '%/Edocs/%' and l.AccessDate > ( @statement_maildate - 1 )
    
            select distinct	lse.name_id,
              case 
                when v.Name_ID is null then ''
                else 'X'
              end as viewed,
              case 
                when v.Name_ID is null then 'X'
                else ''
              end as notviewed,
              case
                when i.Name_ID is null then ''
                else 'X'
              end as viewedInternal
              into #viewed_notviewed
            from LastStatement_Email lse
            left join #viewed_statement v on lse.name_id = v.Name_ID
            left join #viewed_internally i on lse.name_id = i.Name_ID
    
            select distinct l.name_id into #viewed from WebAccessLog l
            where l.Logmsg like '%/Edocs/%' and l.AccessDate > ( @statement_maildate - 1 )
    
            declare @tblcount int;
            select @tblcount = count(*) from sys.all_objects where name = 'swe_viewstatus';
            if @tblcount > 0
                drop table swe_viewstatus;
    
            select v.name_id as account, n.fullName, v.viewed, v.notviewed, v.viewedInternal, vat.tech, b.balance 
            into swe_viewstatus
            from #viewed_notviewed v
            left join name n on v.name_id = n.NAME_ID
            left join v_AcctTech vat on n.NAME_ID = vat.NAME_ID
            left join #Balances b on v.name_id = b.Name_ID
            order by vat.Tech, v.name_id
    
    
            drop table #viewed_statement;
            drop table #viewed;
            drop table #viewed_notviewed;
            drop table #Balances;
            drop table #viewed_internally;
    
            -- select * from swe_viewstatus order by tech, account;
        """
        cursor.execute(cmd)
        conn.commit()
        cursor.close()
        conn.close()
        return

    def load_data(self):
        result = []
        conn = pyodbc.connect(Connection().value())
        cursor = conn.cursor()
        cmd = """ 
            select * from swe_viewstatus order by tech, account;
        """
        try:
            for row in cursor.execute(cmd):
                rowdata = self._extract_row(row)
                record = {
                    'id': rowdata['account'],
                    'name': rowdata['fullname'],
                    'viewed': rowdata['viewed'],
                    'notviewed': rowdata['notviewed'],
                    'viewedinternal': rowdata['viewedinternal'],
                    'tech': rowdata['tech'],
                    'balance': rowdata['balance']
                }
                result.append(record)
        except Exception as e:
            print(str(e))
        self.data = copy.deepcopy(result)
        return


    def _extract_row(self, row):
        r = {}
        i = 0
        for item in row.cursor_description:
            name = item[0]
            val = str(row[i])
            name = name.lower()
            i += 1
            r[name] = val
        return r
