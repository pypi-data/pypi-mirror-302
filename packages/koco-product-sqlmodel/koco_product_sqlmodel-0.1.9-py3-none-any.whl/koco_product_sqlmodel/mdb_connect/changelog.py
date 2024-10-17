from sqlmodel import select, Session, text
import koco_product_sqlmodel.dbmodels.changelog as sql_change
import koco_product_sqlmodel.dbmodels.definition as sql_def
import koco_product_sqlmodel.mdb_connect.mdb_connector as mdb_con
import koco_product_sqlmodel.dbmodels.support as dbm_support
from typing import Any


def get_changes_for_entity_with_id(
    entity_id: int | None,
) -> list[sql_change.CChangelogGet] | None:
    if entity_id == None:
        statement = select(sql_change.CChangelog)
    else:
        statement = select(sql_change.CChangelog).where(
            sql_change.CChangelog.entity_id == entity_id
        )
    res = []
    with Session(mdb_con.mdb_engine) as session:
        results = session.exec(statement=statement).all()
        for r in results:
            return_res = sql_change.CChangelogGet(**r.model_dump())
            return_res.user_name = get_user_name_from_id(
                session=session, user_id=r.user_id
            )
            res.append(return_res)
    return res


def get_user_name_from_id(session: Session = None, user_id: int = None) -> str | None:
    if not user_id:
        return
    if session != None:
        statemnt_user = select(sql_def.CUser.name).where(sql_def.CUser.id == user_id)
        user_name = session.exec(statement=statemnt_user).one_or_none()
        return user_name
    with Session(mdb_con.mdb_engine) as session:
        return get_user_name_from_id(session=session, user_id=user_id)


def get_change_by_id(id: int = None) -> sql_change.CChangelogGet | None:
    statement = select(sql_change.CChangelog).where(sql_change.CChangelog.id == id)
    with Session(mdb_con.mdb_engine) as session:
        res = session.exec(statement=statement).one_or_none()
        if res != None:
            return_res = sql_change.CChangelogGet(**res.model_dump())
            return_res.user_name = get_user_name_from_id(user_id=res.user_id)
            return return_res


def log_results_to_db(
    entity_type: str, entity_id: int, action: str, user_id: int, new_values: str
):
    log_data = sql_change.CChangelog(
        entity_id=entity_id,
        entity_type=entity_type,
        action=action,
        user_id=user_id,
        new_values=new_values,
    )
    # print(log_data)
    with Session(mdb_con.mdb_engine) as session:
        session.add(instance=log_data)
        session.commit()

def write_initial_object_status_to_changelog(db_object: sql_def.SQLModel, user_id: int) -> None:
    log_data = sql_change.CChangelog(
        entity_id=db_object.id,
        entity_type=dbm_support.get_table_from_sqlmodels(model=type(db_object)),
        action='POST',
        user_id=user_id,
        new_values=str(db_object.model_dump_json(exclude=('insdate', 'upddate'))),
        insdate=db_object.insdate
    )
    with Session(mdb_con.mdb_engine) as session:
        session.add(instance=log_data)
        session.commit()


def reset_changelog()->None:
    statement_drop = """
    DROP TABLE IF EXISTS cchangelog;
    """
    statement_create = """
    CREATE TABLE cchangelog (
        id INT NOT NULL AUTO_INCREMENT,
        entity_type VARCHAR(64),
        entity_id INT NOT NULL,
        user_id INT,
        action VARCHAR(64),
        insdate TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        new_values JSON,
        PRIMARY KEY(id)
    );    
    """
    with Session(mdb_con.mdb_engine) as session:
        session.exec(statement=text(statement_drop))
        session.exec(statement=text(statement_create))

def init_changelog(user_id: int) -> None:
    mdb_con.log_initial_status(logfunc = write_initial_object_status_to_changelog, obj_type=sql_def.CCatalog, user_id=user_id)
    mdb_con.log_initial_status(logfunc = write_initial_object_status_to_changelog, obj_type=sql_def.CProductGroup, user_id=user_id)
    mdb_con.log_initial_status(logfunc = write_initial_object_status_to_changelog, obj_type=sql_def.CFamily, user_id=user_id)
    mdb_con.log_initial_status(logfunc = write_initial_object_status_to_changelog, obj_type=sql_def.CArticle, user_id=user_id)
    mdb_con.log_initial_status(logfunc = write_initial_object_status_to_changelog, obj_type=sql_def.CSpecTable, user_id=user_id)
    mdb_con.log_initial_status(logfunc = write_initial_object_status_to_changelog, obj_type=sql_def.CSpecTableItem, user_id=user_id)
    mdb_con.log_initial_status(logfunc = write_initial_object_status_to_changelog, obj_type=sql_def.CApplication, user_id=user_id)
    mdb_con.log_initial_status(logfunc = write_initial_object_status_to_changelog, obj_type=sql_def.COption, user_id=user_id)
    mdb_con.log_initial_status(logfunc = write_initial_object_status_to_changelog, obj_type=sql_def.CUrl, user_id=user_id)
    


def main():
    pass


if __name__ == "__main__":
    main()
