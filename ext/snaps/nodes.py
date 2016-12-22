from datetime import datetime


def workflow_base(uid, *, name):
    return dict(
        bundleid='de.der-beweis.code.master_control.{}'.format(uid),
        category='Productivity',
        createdby='spky',
        description='{} - {}'.format(name, uid),
        disabled=False,
        name='{} (autogenerated)'.format(name),
        readme='master_control - alfred_workflow - {}'.format(uid),
        version=datetime.utcnow().strftime('%Y.%m.%d-%H%M'),
        webaddress='www.der-beweis.de',
    )


def generic_node(uid, *, ptype, config=dict(), version=1):
    return dict(
        config=config,
        type='alfred.workflow.{}'.format(ptype),
        uid=uid,
        version=version,
    )


def connect_nodes(*targets):
    return list(dict(
        destinationuid=target,
        modifiers=0,
        modifiersubtext='',
        vitoclose=False,
    ) for target in targets)


def node_remote(uid, *, name):
    return generic_node(
        uid, config=dict(
            argument='',
            argumenttype=0,
            triggerid=name,
            triggername=name,
            workflowonly=False
        ), ptype='trigger.remote', version=1
    )


def node_script(uid, *, script):
    return generic_node(
        uid, config=dict(
            concurrently=False,
            escaping=102,
            script=script,
            scriptargtype=1,
            scriptfile='',
            type=0,
        ), ptype='action.script', version=2
    )


def node_notification(uid, *, title, text=''):
    return generic_node(
        uid, config=dict(
            lastpathcomponent=False,
            onlyshowifquerypopulated=True,
            removeextension=False,
            text=text,
            title=title,
        ), ptype='output.notification', version=1
    )


def node_arguments(uid, *, argument='', variables=dict()):
    return generic_node(
        uid, config=dict(
            argument=argument,
            variables=variables,
        ), ptype='utility.argument', version=1
    )


def node_keyword(uid, *, keyword, subtext=''):
    return generic_node(
        uid, config=dict(
            argumenttype=2,
            keyword=keyword,
            subtext=subtext,
            text=keyword,
            whitespace=False,
        ), ptype='input.keyword', version=1
    )
