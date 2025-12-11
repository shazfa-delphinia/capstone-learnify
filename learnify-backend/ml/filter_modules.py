def filter_modules_by_lp_and_level(modules_dict, learning_path_name, level):
    out = []
    if not learning_path_name or learning_path_name not in modules_dict:
        return out
    for idx, m in enumerate(modules_dict[learning_path_name]):
        lvl_field = m.get("course_level") or m.get("level") or ""
        if lvl_field.lower().startswith(level.lower()[0:3]):
            # pastikan modul punya module_id & title
            if "module_id" not in m:
                m["module_id"] = f"{learning_path_name}_{idx+1}"
            if "title" not in m:
                m["title"] = m.get("course_name") or m.get("name") or f"Module {idx+1}"
            out.append(m)
    return out
