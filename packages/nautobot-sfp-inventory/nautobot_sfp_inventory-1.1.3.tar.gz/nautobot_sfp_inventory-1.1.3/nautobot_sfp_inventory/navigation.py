from nautobot.core.apps import NavMenuGroup, NavMenuItem, NavMenuTab, NavMenuAddButton

menu_items = (
    NavMenuTab(
        name="Plugins",
        groups=[
            NavMenuGroup(name="SFP Inventory", items=[
                NavMenuItem(
                    link='plugins:nautobot_sfp_inventory:sfptype_list',
                    name="SFP Types",
                    permissions=["dcim.view_sfps"],
                    buttons=[
                        NavMenuAddButton(
                            link='plugins:nautobot_sfp_inventory:sfptype_add',
                            title="Add SFP Type"
                        )
                    ]
                ),
                NavMenuItem(
                    link='plugins:nautobot_sfp_inventory:sfp_list',
                    name="SFPs",
                    permissions=["dcim.view_sfps"],
                    buttons=[
                        NavMenuAddButton(
                            link='plugins:nautobot_sfp_inventory:sfp_add',
                            title="Add SFP"
                        )
                    ]
                ),
            ]),
        ],
    ),
)
