from pyspark.sql.functions import monotonically_increasing_id
from dnalib.utils import TableUtils
from dnalib.log import *
from enum import Enum

class DDL:    
    def __init__(self, layer):
        self.layer = layer.strip().lower()    

class ObjectDDL(DDL):

    def __init__(self, layer):
        super().__init__(layer)      

    def describe(self):
        raise NotImplementedError("Method create() must be implemented.")    

    def create_table(self):
        raise NotImplementedError("Method create_table() must be implemented.")    

    def create_view(self):
        raise NotImplementedError("Method create_view() must be implemented.")    
        
    def drop(self):
        raise NotImplementedError("Method drop() must be implemented.")        

class Table(ObjectDDL):

    def __init__(self, 
                 layer, 
                 table_name, 
                 yml={}, 
                 partition_fields=[],                               
                 fields={},
                 tbl_properties={},
                 replace=False):
        super().__init__(layer)
        self.table_name = table_name.strip().lower()    
        self.yml = yml
        self.table_path = Utils.lakehouse_path(self.layer, self.table_name) 
        self.yml = yml
        if isinstance(self.yml, str):
            self.yml = Utils.safe_load_and_parse_yml(yml)
        self.partition_fields = self.yml.get("partition_fields", partition_fields)         
        self.fields = self.yml.get("fields", fields)        
        self.tbl_properties = self.yml.get("tbl_properties", tbl_properties)                
        self.replace = replace
        self.parsed_template_table = ""
        self.parsed_fields = "" 
        self.parsed_tbl_properties = "" 
        self.parsed_partition_fields = ""

    def populate_tbl_properties(self):                  
        if len(self.tbl_properties) == 0:
            df_tbl_properties = Utils.spark_instance().sql(f"SHOW TBLPROPERTIES {self.layer}.{self.table_name}")
            self.tbl_properties = df_tbl_properties.rdd.map(lambda property : (property[0], property[1])).collectAsMap()
        return self.tbl_properties        

    def populate_partition_fields(self):
        if len(self.partition_fields) == 0:
            df_describe = df_describe = self.describe()
            df_rowIdInit = df_describe.filter("col_name like '# Partition Information%'").select('rowId')            
            if df_rowIdInit.count() > 0:
                rowIdInit = df_rowIdInit.first()[0]+1
                rowIdEnd = df_describe.filter(f"(rowId > {rowIdInit}) and col_name like ''").select('rowId').first()[0]
                df_partitions = df_describe.filter(f"(rowId > {rowIdInit}) and (rowId < {rowIdEnd})").select('col_name')
                self.partition_fields = df_partitions.rdd.flatMap(list).collect()
        return self.partition_fields

    def populate_fields(self):
        if len(self.fields) == 0:
            df_describe = self.describe()
            rowId = df_describe.filter("col_name like '#%'").select('rowId').first()[0]  
            df_fields = df_describe.filter(f"(rowId < {rowId}) and col_name != ''").drop('rowId')
            self.fields = df_fields.rdd.map(lambda field : (field[0], [field[2], field[1]])).collectAsMap()
        return self.fields
    
    def parse_tbl_properties(self):
        self.populate_tbl_properties()
        if len(self.tbl_properties) > 0:
            tbl_properties_content = ", ".join([f"{key}='{value}'" for key, value in self.tbl_properties.items()])
            self.parsed_tbl_properties = f"TBLPROPERTIES ({tbl_properties_content})"
        return self.parsed_tbl_properties
    
    def parse_partition_fields(self):
        self.populate_partition_fields()
        if len(self.partition_fields) > 0:
            partition_fields_content = ", ".join(self.partition_fields)
            self.parsed_partition_fields = f"PARTITIONED BY ({partition_fields_content})"
        return self.parsed_partition_fields

    def describe(self):        
        return TableUtils.describe_table(self.layer, self.table_name)

    def drop(self):
        return TableUtils.drop_table(self.layer, self.table_name)
    
    def template_table(self):
        # generate template for create table
        self.parsed_template_table = """
            CREATE OR REPLACE TABLE {}.{} (
                {}
            )
            USING delta
            {}
            {}
            LOCATION '{}'
        """.format(self.layer, self.table_name, self.parsed_fields, self.parse_tbl_properties(), self.parse_partition_fields(), self.table_path)
        return self    
    
    def create_table(self):
        if not TableUtils.table_exists(self.layer, self.table_name) or self.replace:                 
            ## generate final create table template
            self.template() 
            Utils.spark_instance().sql(self.parsed_template_table)                                            
            # mark table has been created or replaced by class
            self.has_created_table = True    
        else:
            log(__name__).warning(f"The table already exists, so nothing will be done.")
        return self
    
class BronzeTable(Table):

    layer = "bronze"

    def __init__(self,                  
                 table_name, 
                 yml={},                  
                 partition_fields=[],                                              
                 fields={},
                 tbl_properties={}):
        super().__init__(self.layer, table_name, yml, partition_fields, fields, tbl_properties)        

class SilverTable(Table):

    table_comment_keywords = {
        'descricao': '- **Descrição**:',
        'sistema_origem': '- **Sistema Origem**:',
        'calendario': '- **Calendário de Disponibilização**:',
        'tecnologia': '- **Tecnologia Sistema Origem**:',
        'camada': '- **Camada de Dados**:',
        'peridiocidade': '- **Periodicidade de Atualização**:',
        'retencao': '- **Período de Retenção**:',
        'vertical': '- **Vertical**:',
        'dominio': '- **Domínio**:',
        'squad': '- **Squad Responsável**:',
        'categoria_portosdm': '- **Categoria e Grupo PortoSDM**:',
        'confidencialidade': '- **Classificação da Confidencialidade**:',
        'classificacao': '- **Classificação**:',
        'campos_anonimizados': '- **Campos Anonimizados**:',
        'deprecated': '- **Deprecated**:'
    }

    table_squad_keywords = {
        'gi': '- **GI - Gestor da Informação**:',
        'gdn': '- **GDN - Gestor de Negócio**:',
        'curador': '- **Curador**:',
        'custodiante': '- **Custodiante**:',
    }

    table_comment_atlan_pattern =  {
        'descricao': '- **Descrição**:',
        'sistema_origem': '- **Sistema Origem**:',
        'calendario': '- **Calendário de Disponibilização**:',
        'tecnologia': '- **Tecnologia Sistema Origem**:',
        'camada': '- **Camada de Dados**:',
        'peridiocidade': '- **Periodicidade de Atualização**:',
        'retencao': '- **Período de Retenção**:',
        'vertical': '- **Vertical**:',
        'dominio': '- **Domínio**:',
        'gi': '- **GI - Gestor da Informação**:',
        'gdn': '- **GDN - Gestor de Negócio**:',
        'curador': '- **Curador**:',
        'custodiante': '- **Custodiante**:',
        'squad': '- **Squad Responsável**:',
        'categoria_portosdm': '- **Categoria e Grupo PortoSDM**:',
        'confidencialidade': '- **Classificação da Confidencialidade**:',
        'classificacao': '- **Classificação**:',
        'campos_anonimizados': '- **Campos Anonimizados**:',
        'deprecated': '- **Deprecated**:'
    }

    layer = "silver"

    def __init__(self,                  
                 table_name, 
                 yml={}, 
                 anonimized_fields=[],  
                 partition_fields=[],                                              
                 fields={},
                 tbl_properties={}):
        super().__init__(self.layer, table_name, yml, partition_fields, fields, tbl_properties)
        self.anonimized_fields = self.yml.get("anonimized_fields", anonimized_fields)       
            


