
def summary(jira, issue_id):
    issue = jira.issue(issue_id, fields="summary")
    return "`%s`" % issue.fields.summary


def comments(jira, issue_id):
    issue = jira.issue(issue_id, fields="comment")
    return "\n\r\n\r".join(
        ["`%s`" % comment.body for comment in issue.fields.comment.comments]
    )


def test(jira, issue_id):
    issue = jira.issue(issue_id)
    import pdb;pdb.set_trace()

