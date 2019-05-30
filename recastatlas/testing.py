import yadageschemas


def validate_entry(data):
    toplevel = data["spec"]["toplevel"]
    workflow = data["spec"]["workflow"]
    try:
        yadageschemas.load(
            workflow,
            specopts={
                "toplevel": toplevel,
                "load_as_ref": False,
                "schema_name": "yadage/workflow-schema",
                "schemadir": yadageschemas.schemadir,
            },
            validopts={
                "schemadir": yadageschemas.schemadir,
                "schema_name": "yadage/workflow-schema",
            },
        )
        return True
    except:
        pass
    return False
