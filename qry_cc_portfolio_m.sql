SELECT tbl_advisor_last_fact.SM AS 1SM, tbl_advisor_last_fact.SM_NAME AS 1SM_NAME, tbl_advisor_last_fact.M AS 1M, tbl_advisor_last_fact.M_NAME AS 1M_NAME, tbl_advisor_last_fact.DM, tbl_advisor_last_fact.DM_NAME, qry_CC_Portfolio.*
FROM qry_CC_Portfolio LEFT JOIN tbl_advisor_last_fact ON qry_CC_Portfolio.AMSup=tbl_advisor_last_fact.AMSup;
