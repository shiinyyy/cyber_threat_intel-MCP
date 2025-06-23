from taxii2client.v21 import Server

# Global cache for MITRE ATT&CK data
all_mitre_objects = None
objects_by_id = None


def get_data():
    """
    Connects to the MITRE server and loads the entire dataset into memory.
    """
    global all_mitre_objects, objects_by_id
    if all_mitre_objects is not None:
        return  # Data is already cached

    print("Connecting to MITRE ATT&CK server...")
    try:
        server = Server("https://attack-taxii.mitre.org/taxii2/")
        api_root = server.api_roots[0]
        collection = next(
            (c for c in api_root.collections if c.title == "Enterprise ATT&CK"), None
        )
        if not collection:
            raise RuntimeError("Enterprise ATT&CK collection not found.")
    except Exception as e:
        print(f"Failed to connect to server or find collection: {e}")
        # Mark as loaded but empty to prevent retries
        all_mitre_objects = []
        objects_by_id = {}
        return

    print("Fetching all Enterprise ATT&CK data. This may take a moment...")
    all_objects = collection.get_objects()["objects"]
    all_mitre_objects = all_objects
    objects_by_id = {obj["id"]: obj for obj in all_objects}
    print(f"Successfully retrieved {len(all_mitre_objects)} objects.")


# Defining tools
def find_group_object(group_name: str):
    """A function to find the group object."""
    get_data()
    if not all_mitre_objects:
        return None

    print(f"Searching for group: '{group_name}' in cached data...")
    for obj in all_mitre_objects:
        if obj.get("type") == "intrusion-set":
            # Match on name or alias
            if group_name.lower() == obj.get("name", "").lower() or group_name.lower() in [
                alias.lower() for alias in obj.get("aliases", [])
            ]:
                print(f"Found group: {obj.get('name')}")
                return obj
    print(f"Group '{group_name}' not found in cached data.")
    return None


def get_group_description(group_name: str) -> str:
    """Gets the detailed description for a specific threat group."""
    group_object = find_group_object(group_name)
    if not group_object:
        return f"Group '{group_name}' not found."
    return group_object.get("description", "No description available for this group.")


def get_group_techniques(group_name: str) -> list[str]:
    """Gets the names of all techniques used by a specific threat group."""
    group_object = find_group_object(group_name)
    if not group_object:
        return [f"Group '{group_name}' not found."]

    technique_ids = set()
    for obj in all_mitre_objects:
        if (
            obj.get("type") == "relationship"
            and obj.get("source_ref") == group_object.get("id")
            and obj.get("relationship_type") == "uses"
            and "attack-pattern" in obj.get("target_ref", "")
        ):
            technique_ids.add(obj["target_ref"])

    if not technique_ids:
        return [f"No techniques found for group '{group_name}'."]

    techniques = [objects_by_id.get(tid) for tid in technique_ids]
    return sorted([t.get("name") for t in techniques if t and t.get("name")])


def get_group_campaigns(group_name: str) -> list[str]:
    """Gets the names of all campaigns attributed to a specific threat group."""
    group_object = find_group_object(group_name)
    if not group_object:
        return [f"Group '{group_name}' not found."]

    campaign_ids = set()
    for obj in all_mitre_objects:
        if (
            obj.get("type") == "relationship"
            and obj.get("target_ref") == group_object.get("id")
            and obj.get("relationship_type") == "attributed-to"
        ):
            campaign_ids.add(obj["source_ref"])

    if not campaign_ids:
        return [f"No campaigns found for group '{group_name}'."]

    campaigns = [objects_by_id.get(cid) for cid in campaign_ids]
    return sorted([c.get("name") for c in campaigns if c and c.get("name")])


# #  testing
# if __name__ == "__main__":
#     # Pass group name as a parameter
#     target_group = "APT29"
#     intel = get_group_intel(target_group)

#     if intel:
#         print("\n" + "=" * 50)
#         print(f"CTI report for: {intel['group'].get('name')}")
#         print("=" * 50)
#         print(f"\nDescription:\n{intel['group'].get('description')}")
        
#         print("\n__Associated Campaigns__")
#         if intel["campaigns"]:
#             for campaign in sorted(intel["campaigns"], key=lambda x: x.get("name", "")):
#                 print(f"- {campaign.get('name')}")
#         else:
#             print("No campaign found under this group")
            
#         print("\n__Technique Used__")
#         if intel["techniques"]:
#             for tech in sorted(intel["techniques"], key=lambda x: x.get("name", "")):
#                 external_id = tech.get("external_references", [{}])[0].get(
#                     "external_id", "N/A"
#                 )
#                 print(f"- {tech.get('name')} ({external_id})")
#         else:
#             print("No techniques found for this group.")
            