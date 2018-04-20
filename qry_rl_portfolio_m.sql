SELECT advisor_last_fact.SM AS 1SM, advisor_last_fact.SM_NAME AS 1SM_NAME, advisor_last_fact.M AS 1M, advisor_last_fact.M_NAME AS 1M_NAME, advisor_last_fact.DM, advisor_last_fact.DM_NAME, qry_RL_Portfolio.*
FROM qry_RL_Portfolio LEFT JOIN advisor_last_fact ON qry_RL_Portfolio.AMSup=advisor_last_fact.AMSup;
