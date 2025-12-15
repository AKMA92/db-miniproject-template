import streamlit as st
from sqlalchemy import text


def get_connection():
    return st.connection("postgresql", type="sql")


# =========================================================
# COMPANY – SQL-Funktionen
# =========================================================

def select_companies():
    conn = get_connection()
    sql = """
        SELECT
            company_id,
            name,
            company_type,
            email,
            telephone_number,
            address
        FROM company;
    """
    return conn.query(sql, ttl=0)


def insert_company(company_id, name, company_type, email, telephone_number, address):
    conn = get_connection()
    sql = """
        INSERT INTO company (company_id, name, company_type, email, telephone_number, address)
        VALUES (:company_id, :name, :company_type, :email, :telephone_number, :address)
    """
    with conn.session as s:
        s.execute(
            text(sql),
            {
                "company_id": int(company_id),
                "name": name,
                "company_type": company_type,
                "email": email,
                "telephone_number": telephone_number,
                "address": address,
            },
        )
        s.commit()


def update_company(company_id, name, company_type, email, telephone_number, address):
    conn = get_connection()
    sql = """
        UPDATE company
        SET name = :name,
            company_type = :company_type,
            email = :email,
            telephone_number = :telephone_number,
            address = :address
        WHERE company_id = :company_id
    """
    with conn.session as s:
        res = s.execute(
            text(sql),
            {
                "company_id": int(company_id),
                "name": name,
                "company_type": company_type,
                "email": email,
                "telephone_number": telephone_number,
                "address": address,
            },
        )
        if res.rowcount == 0:
            s.rollback()
            raise ValueError(f"Keine Firma mit company_id={company_id} gefunden.")
        s.commit()


def delete_company(company_id: int):
    conn = get_connection()

    sql_get_emp_ids = """
        SELECT employee_id
        FROM employed
        WHERE company_id = :company_id
    """

    sql_delivered = """
        DELETE from delivered
        WHERE company_id = :company_id
    """

    sql_employed = """
        DELETE FROM employed
        WHERE company_id = :company_id
    """

    sql_delete_employees = """
        DELETE FROM employee
        WHERE employee_id = ANY(:emp_ids)
    """

    sql_delete_company = """
        DELETE FROM company
        WHERE company_id = :company_id
    """

    with conn.session as s:
        emp_rows = s.execute(text(sql_get_emp_ids), {"company_id": int(company_id)}).fetchall()
        emp_ids = [r[0] for r in emp_rows]

        s.execute(text(sql_delivered), {"company_id": int(company_id)})
        s.execute(text(sql_employed), {"company_id": int(company_id)})

        if emp_ids:
            s.execute(text(sql_delete_employees), {"emp_ids": emp_ids})

        res = s.execute(text(sql_delete_company), {"company_id": int(company_id)})
        if res.rowcount == 0:
            s.rollback()
            raise ValueError(f"Keine Firma mit company_id={company_id} gefunden.")

        s.commit()


# =========================================================
# EMPLOYEE – SQL-Funktionen
# =========================================================

def select_employees():
    conn = get_connection()
    sql = """
        SELECT
          e.employee_id,
          c.company_id,
          e.first_name,
          e.last_name,
          e.email,
          e.telephone_number,
          c.name AS company_name
        FROM employee e
        JOIN employed em ON em.employee_id = e.employee_id
        JOIN company c ON c.company_id = em.company_id;
    """
    return conn.query(sql, ttl=0)


def insert_employee(employee_id, company_id, first_name, last_name, email, telephone_number):
    conn = get_connection()

    sql_employee = """
        INSERT INTO employee (employee_id, first_name, last_name, email, telephone_number)
        VALUES (:employee_id, :first_name, :last_name, :email, :telephone_number)
    """

    sql_employed = """
        INSERT INTO employed (employee_id, company_id)
        VALUES (:employee_id, :company_id)
    """

    with conn.session as s:
        s.execute(
            text(sql_employee),
            {
                "employee_id": int(employee_id),
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "telephone_number": telephone_number,
            },
        )

        s.execute(
            text(sql_employed),
            {
                "employee_id": int(employee_id),
                "company_id": int(company_id),
            },
        )

        s.commit()

def update_employee(employee_id, company_id, first_name, last_name, email, telephone_number):
    conn = get_connection()

    sql_employee = """
        UPDATE employee
        SET first_name = :first_name,
            last_name = :last_name,
            email = :email,
            telephone_number = :telephone_number
        WHERE employee_id = :employee_id
    """

    sql_employed = """
        UPDATE employed
        SET company_id = :company_id
        WHERE employee_id = :employee_id
    """

    with conn.session as s:
        s.execute(
            text(sql_employee),
            {
                "employee_id": int(employee_id),
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "telephone_number": telephone_number,
            },
        )

        s.execute(
            text(sql_employed),
            {
                "employee_id": int(employee_id),
                "company_id": int(company_id),
            },
        )

        s.commit()


def delete_employee(employee_id: int):
    conn = get_connection()

    sql_employed = """
        DELETE FROM employed
        WHERE employee_id = :employee_id
    """
    sql_employee = """
        DELETE FROM employee
        WHERE employee_id = :employee_id
    """

    with conn.session as s:
        s.execute(text(sql_employed), {"employee_id": int(employee_id)})
        res = s.execute(text(sql_employee), {"employee_id": int(employee_id)})
        if res.rowcount == 0:
            s.rollback()
            raise ValueError(f"Kein Mitarbeiter mit employee_id={employee_id} gefunden.")
        s.commit()


# =========================================================
# PRODUCT – SQL-Funktionen
# =========================================================

def select_products():
    conn = get_connection()
    sql = """
        SELECT
          product_id,
          name,
          category,
          product_type
        FROM product;
    """
    return conn.query(sql, ttl=0)


def insert_product(product_id, company_id, name, category, product_type):
    conn = get_connection()

    sql_product = """
        INSERT INTO product (product_id, name, category, product_type)
        VALUES (:product_id, :name, :category, :product_type)
    """

    sql_delivered = """
        INSERT INTO delivered (product_id, company_id)
        VALUES (:product_id, :company_id)
    """

    with conn.session as s:
        s.execute(
            text(sql_product),
            {
                "product_id": int(product_id),
                "name": name,
                "category": category,
                "product_type": product_type,
            },
        )
        s.execute(
            text(sql_delivered),
            {
                "product_id": int(product_id),
                "company_id": int(company_id),
            },
        )
        s.commit()


def update_product(product_id, name, category, product_type):
    conn = get_connection()
    sql = """
        UPDATE product
        SET name = :name,
            category = :category,
            product_type = :product_type
        WHERE product_id = :product_id
    """
    with conn.session as s:
        s.execute(
            text(sql),
            {
                "product_id": int(product_id),
                "name": name,
                "category": category,
                "product_type": product_type,
            },
        )
        s.commit()


def delete_product(product_id: int):
    conn = get_connection()

    sql_delivered = "DELETE from delivered WHERE product_id = :product_id"
    sql_product = "DELETE FROM product WHERE product_id = :product_id"

    with conn.session as s:
        s.execute(text(sql_delivered), {"product_id": int(product_id)})
        res = s.execute(text(sql_product), {"product_id": int(product_id)})
        if res.rowcount == 0:
            s.rollback()
            raise ValueError(f"Kein Produkt mit product_id={product_id} gefunden.")
        s.commit()


# =========================================================
# Seiten / Tabs
# =========================================================

def page_overview():
    st.subheader("Übersicht")
    st.write("""
        Mein ER-Diagramm zeigt die Entität Company, die in einer 1-m-Beziehung zu Employee steht, realisiert über die Zwischentabelle Employed, wobei jeder Mitarbeiter genau einer Firma zugeordnet ist.
        Zwischen Company und Product besteht eine n-m-Beziehung, die über die Tabelle Deliver abgebildet wird, da eine Firma mehrere Produkte liefern kann und ein Produkt von mehreren Firmen geliefert werden kann.
    """)

    st.image(
        "er-design-mini-project.png",
        caption="ER-Diagramm der Datenbankstruktur",
        use_container_width=True
    )


def page_companies():
    st.markdown("#### Firmen anzeigen")
    companies = select_companies()
    if companies is None or companies.empty:
        st.info("Keine Firmen gefunden.")
    else:
        st.dataframe(
            companies,
            column_config={
                "company_id": "Firma-ID",
                "name": "Name",
                "company_type": "Typ",
                "email": "E-Mail",
                "telephone_number": "Telefonnummer",
                "address": "Adresse",
            },
            use_container_width=True,
        )

    st.markdown("#### Neue Firma einfügen")
    with st.form("form_add_company"):
        company_id = st.text_input("Firma-ID")
        name = st.text_input("Name")
        company_type = st.selectbox("Typ", ("Supplier", "Customer", "Own"))
        email = st.text_input("E-Mail")
        telephone_number = st.text_input("Telefonnummer")
        address = st.text_area("Adresse")

        submitted = st.form_submit_button("Firma speichern")
        if submitted:
            insert_company(company_id, name, company_type, email, telephone_number, address)
            st.success("Firma erfolgreich hinzugefügt.")
            st.rerun()

    st.markdown("#### Firma aktualisieren")

    companies = select_companies()
    if companies is None or companies.empty:
        st.info("Keine Firmen zum Aktualisieren vorhanden.")
    else:
        companies = companies.copy()
        companies["display"] = companies["company_id"].astype(str) + " – " + companies["name"].astype(str)

        selected_display_upd = st.selectbox(
            "Firma auswählen (Update)",
            options=companies["display"].tolist(),
            key="update_company_select",
        )

        row = companies[companies["display"] == selected_display_upd].iloc[0]
        cid = int(row["company_id"])

        options_company_type = ("Supplier", "Customer", "Own")
        current_type = str(row["company_type"]).strip()
        if current_type not in options_company_type:
            current_type = "Supplier"
        current_type_index = options_company_type.index(current_type)

        with st.form("form_update_company"):
            upd_name = st.text_input("Name", value=str(row["name"]))
            upd_company_type = st.selectbox("Typ", options_company_type, index=current_type_index)
            upd_email = st.text_input("E-Mail", value=str(row["email"]))
            upd_telephone_number = st.text_input("Telefonnummer", value=str(row["telephone_number"]))
            upd_address = st.text_area("Adresse", value=str(row["address"]))

            submitted_upd = st.form_submit_button("Firma aktualisieren")

            if submitted_upd:
                try:
                    update_company(cid, upd_name, upd_company_type, upd_email, upd_telephone_number, upd_address)
                    st.success("Firma erfolgreich aktualisiert.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Update fehlgeschlagen: {e}")

    st.markdown("#### Firma löschen")

    companies = select_companies()
    if companies is None or companies.empty:
        st.info("Keine Firmen zum Löschen vorhanden.")
        return

    companies = companies.copy()
    companies["display"] = companies["company_id"].astype(str) + " – " + companies["name"].astype(str)

    selected_display = st.selectbox("Firma auswählen", options=companies["display"].tolist(), key="delete_company_select")
    selected_row = companies[companies["display"] == selected_display].iloc[0]
    selected_company_id = int(selected_row["company_id"])

    conn = get_connection()
    sql_counts = """
        SELECT
          (SELECT COUNT(*) FROM employed  WHERE company_id = :cid) AS employed_count,
          (SELECT COUNT(*) from delivered WHERE company_id = :cid) AS delivered_count
    """
    counts = conn.query(sql_counts, params={"cid": selected_company_id}, ttl=0)
    employed_count = int(counts.iloc[0]["employed_count"])
    delivered_count = int(counts.iloc[0]["delivered_count"])

    st.warning(
        f"Beim Löschen wird **die Firma** entfernt und zusätzlich:\n"
        f"- **{employed_count}** Mitarbeiter (inkl. Zuordnung)\n"
        f"- **{delivered_count}** Lieferbeziehungen (Delivered)\n\n"
        f"Dieser Vorgang ist nicht rückgängig zu machen."
    )

    confirm = st.checkbox("Ich bestätige das endgültige Löschen dieser Firma inkl. Mitarbeitenden und Beziehungen.",
                          key="delete_company_confirm")

    delete_clicked = st.button("🗑️ Firma endgültig löschen", disabled=not confirm, type="primary", key="delete_company_btn")

    if delete_clicked:
        try:
            delete_company(selected_company_id)
            st.success("Firma erfolgreich gelöscht (inkl. Mitarbeitenden & Beziehungen).")
            st.rerun()
        except Exception as e:
            st.error(f"Löschen fehlgeschlagen: {e}")


def page_employees():

    st.markdown("#### Mitarbeiter anzeigen")
    employees = select_employees()
    if employees is None or employees.empty:
        st.info("Keine Mitarbeiter gefunden.")
    else:
        st.dataframe(
            employees,
            column_config={
                "employee_id": "Mitarbeiter-ID",
                "company_id": "Firma-ID",
                "first_name": "Vorname",
                "last_name": "Nachname",
                "email": "E-Mail",
                "telephone_number": "Telefonnummer",
                "company_name": "Firma",
            },
            use_container_width=True,
        )

    st.markdown("#### Neuen Mitarbeiter einfügen")
    with st.form("form_add_employee"):
        employee_id = st.number_input("Mitarbeiter-ID", min_value=1, step=1)
        company_id = st.number_input("Firma-ID", min_value=1, step=1)
        first_name = st.text_input("Vorname")
        last_name = st.text_input("Nachname")
        email = st.text_input("E-Mail")
        telephone_number = st.text_input("Telefonnummer")

        submitted = st.form_submit_button("Mitarbeiter speichern")
        if submitted:
            insert_employee(employee_id, company_id, first_name, last_name, email, telephone_number)
            st.success("Mitarbeiter erfolgreich hinzugefügt.")
            st.rerun()

    st.markdown("#### Mitarbeiter aktualisieren")

    employees = select_employees()
    if employees is None or employees.empty:
        st.info("Keine Mitarbeiter zum Aktualisieren vorhanden.")
    else:
        employees = employees.copy()
        employees["display"] = (
            employees["employee_id"].astype(str)
            + " – "
            + employees["first_name"].astype(str)
            + " "
            + employees["last_name"].astype(str)
            + " ("
            + employees["company_name"].astype(str)
            + ")"
        )

        selected_display_upd = st.selectbox(
            "Mitarbeiter auswählen (Update)",
            options=employees["display"].tolist(),
            key="update_employee_select",
        )

        row = employees[employees["display"] == selected_display_upd].iloc[0]
        eid = int(row["employee_id"])

        with st.form("form_update_employee"):
            upd_company_id = st.number_input("Firma-ID", min_value=1, step=1, value=int(row["company_id"]))
            upd_first_name = st.text_input("Vorname", value=str(row["first_name"]))
            upd_last_name = st.text_input("Nachname", value=str(row["last_name"]))
            upd_email = st.text_input("E-Mail", value=str(row["email"]))
            upd_telephone_number = st.text_input("Telefonnummer", value=str(row["telephone_number"]))

            submitted_upd = st.form_submit_button("Mitarbeiter aktualisieren")

            if submitted_upd:
                try:
                    update_employee(eid, upd_company_id, upd_first_name, upd_last_name, upd_email, upd_telephone_number)
                    st.success("Mitarbeiter erfolgreich aktualisiert.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Update fehlgeschlagen: {e}")

    st.markdown("#### Mitarbeiter löschen")

    employees = select_employees()
    if employees is None or employees.empty:
        st.info("Keine Mitarbeiter zum Löschen vorhanden.")
        return

    employees = employees.copy()
    employees["display"] = (
        employees["employee_id"].astype(str)
        + " – "
        + employees["first_name"].astype(str)
        + " "
        + employees["last_name"].astype(str)
        + " ("
        + employees["company_name"].astype(str)
        + ")"
    )

    selected_display = st.selectbox("Mitarbeiter auswählen", options=employees["display"].tolist(),
                                    key="delete_employee_select")
    selected_row = employees[employees["display"] == selected_display].iloc[0]
    selected_employee_id = int(selected_row["employee_id"])

    st.warning(
        "Beim Löschen wird der Mitarbeiter **endgültig** entfernt.\n\n"
        "Dieser Vorgang ist nicht rückgängig zu machen."
    )

    confirm = st.checkbox("Ich bestätige das endgültige Löschen dieses Mitarbeiters.", key="delete_employee_confirm")
    delete_clicked = st.button("🗑️ Mitarbeiter endgültig löschen", disabled=not confirm, type="primary",
                               key="delete_employee_btn")

    if delete_clicked:
        try:
            delete_employee(selected_employee_id)
            st.success("Mitarbeiter erfolgreich gelöscht.")
            st.rerun()
        except Exception as e:
            st.error(f"Löschen fehlgeschlagen: {e}")


def page_products():
    st.markdown("#### Produkte anzeigen")
    products = select_products()
    if products is None or products.empty:
        st.info("Keine Produkte gefunden.")
    else:
        st.dataframe(
            products,
            column_config={
                "product_id": "Produkt-ID",
                "name": "Name",
                "category": "Kategorie",
                "product_type": "Typ",
            },
            use_container_width=True,
        )

    st.markdown("#### Neues Produkt einfügen")
    with st.form("form_add_product"):
        product_id = st.number_input("Produkt-ID", min_value=1, step=1)
        company_id = st.number_input("Firma-ID (Lieferant)", min_value=1, step=1)
        name = st.text_input("Produktname")
        category = st.selectbox("Kategorie", ("food", "hygiene", "garden", "electronics", "other"))
        product_type = st.text_input("Produkttyp")

        submitted = st.form_submit_button("Produkt speichern")
        if submitted:
            insert_product(product_id, company_id, name, category, product_type)
            st.success("Produkt erfolgreich hinzugefügt.")
            st.rerun()

    st.markdown("#### Produkt aktualisieren")

    products = select_products()
    if products is None or products.empty:
        st.info("Keine Produkte zum Aktualisieren vorhanden.")
    else:
        products = products.copy()
        products["display"] = products["product_id"].astype(str) + " – " + products["name"].astype(str)

        selected_display_upd = st.selectbox(
            "Produkt auswählen (Update)",
            options=products["display"].tolist(),
            key="update_product_select",
        )

        row = products[products["display"] == selected_display_upd].iloc[0]
        pid = int(row["product_id"])

        category_options = ("food", "hygiene")
        current_category = str(row["category"]).strip().lower()
        if current_category not in category_options:
            current_category = "food"
        current_category_index = category_options.index(current_category)

        current_product_type = "" if row["product_type"] is None else str(row["product_type"])

        with st.form("form_update_product"):
            upd_name = st.text_input("Produktname", value=str(row["name"]))
            upd_category = st.selectbox("Kategorie", category_options, index=current_category_index)
            upd_product_type = st.text_input("Produkttyp", value=current_product_type)

            submitted_upd = st.form_submit_button("Produkt aktualisieren")

            if submitted_upd:
                try:
                    update_product(pid, upd_name, upd_category, upd_product_type)
                    st.success("Produkt erfolgreich aktualisiert.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Update fehlgeschlagen: {e}")

    st.markdown("#### Produkt löschen")

    products = select_products()
    if products is None or products.empty:
        st.info("Keine Produkte zum Löschen vorhanden.")
        return

    products = products.copy()
    products["display"] = products["product_id"].astype(str) + " – " + products["name"].astype(str)

    selected_display = st.selectbox("Produkt auswählen", options=products["display"].tolist(), key="delete_product_select")
    selected_row = products[products["display"] == selected_display].iloc[0]
    selected_product_id = int(selected_row["product_id"])

    conn = get_connection()
    sql_count_delivered = """
        SELECT COUNT(*) AS delivered_count
        from delivered
        WHERE product_id = :pid
    """
    delivered_count_df = conn.query(sql_count_delivered, params={"pid": selected_product_id}, ttl=0)
    delivered_count = int(delivered_count_df.iloc[0]["delivered_count"])

    st.warning(
        f"Beim Löschen wird das Produkt **endgültig** entfernt und zusätzlich:\n"
        f"- **{delivered_count}** Lieferbeziehungen (Delivered)\n\n"
        f"Dieser Vorgang ist nicht rückgängig zu machen."
    )

    confirm = st.checkbox("Ich bestätige das endgültige Löschen dieses Produkts inkl. Lieferbeziehungen.",
                          key="delete_product_confirm")

    delete_clicked = st.button("🗑️ Produkt endgültig löschen", disabled=not confirm, type="primary", key="delete_product_btn")

    if delete_clicked:
        try:
            delete_product(selected_product_id)
            st.success("Produkt erfolgreich gelöscht (inkl. Lieferbeziehungen).")
            st.rerun()
        except Exception as e:
            st.error(f"Löschen fehlgeschlagen: {e}")

def page_ddls():
    st.subheader("DDL – Datenbankstruktur")

    ddl_code = """
    -- ==========================================
    -- SQL DDL Statements
    -- ==========================================

    DROP TABLE IF EXISTS DELIVER CASCADE;
    DROP TABLE IF EXISTS DELIVERED CASCADE;
    DROP TABLE IF EXISTS EMPLOYED CASCADE;
    DROP TABLE IF EXISTS PRODUCT CASCADE;
    DROP TABLE IF EXISTS EMPLOYEE CASCADE;
    DROP TABLE IF EXISTS COMPANY CASCADE;

    CREATE TABLE COMPANY (
        company_id        INTEGER PRIMARY KEY,
        name              VARCHAR(100) NOT NULL,
        company_type      VARCHAR(100) NOT NULL,
        email             VARCHAR(255) NOT NULL,
        telephone_number  VARCHAR(50) NOT NULL,
        address           TEXT NOT NULL,
        CONSTRAINT uq_company_email UNIQUE (email),
        CONSTRAINT chk_company_email CHECK (email ~ '^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$'),
        CONSTRAINT chk_company_type CHECK (company_type IN ('Supplier','Customer','Own'))
    );

    CREATE TABLE EMPLOYEE (
        employee_id       INTEGER PRIMARY KEY,
        first_name        VARCHAR(100) NOT NULL,
        last_name         VARCHAR(100) NOT NULL,
        email             VARCHAR(255) NOT NULL,
        telephone_number  VARCHAR(50) NOT NULL,
        CONSTRAINT uq_employee_email UNIQUE (email),
        CONSTRAINT chk_employee_email CHECK (email ~ '^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$')
    );

    CREATE TABLE PRODUCT (
        product_id    INTEGER PRIMARY KEY,
        name          VARCHAR(100) NOT NULL,
        category      VARCHAR(100) NOT NULL,
        product_type  VARCHAR(100) NULL,
        CONSTRAINT chk_product_category CHECK (category IN ('food','hygiene', 'garden', 'electronics', 'other'))
    );

    CREATE TABLE EMPLOYED (
        employee_id INT PRIMARY KEY REFERENCES EMPLOYEE (employee_id),
        company_id  INT NOT NULL REFERENCES COMPANY (company_id)
    );

    CREATE TABLE DELIVER (
        product_id INT NOT NULL REFERENCES PRODUCT (product_id),
        company_id INT NOT NULL REFERENCES COMPANY (company_id),
        PRIMARY KEY (product_id, company_id)
    );
    """

    st.code(ddl_code, language="sql")

def main():
    st.title("Mini-Projekt-Migros")

    tab_overview, tab_companies, tab_employees, tab_products, tab_ddls = st.tabs(
        ["Übersicht", "Firmen", "Mitarbeiter", "Produkte", "DDLs"]
    )

    with tab_overview:
        page_overview()

    with tab_companies:
        page_companies()

    with tab_employees:
        page_employees()

    with tab_products:
        page_products()

    with tab_ddls:
        page_ddls()

if __name__ == "__main__":
    main()
