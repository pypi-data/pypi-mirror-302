"""Module for registering CLI plugins for jaseci."""

import json
import os
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from uvicorn import run
from bson import ObjectId
from jaclang.cli.cmdreg import cmd_registry
from jaclang.plugin.default import hookimpl
from jac_cloud.plugin.jaseci import NodeAnchor
from fastapi.middleware.cors import CORSMiddleware


class JacCmd:
    """Jac CLI."""

    @staticmethod
    @hookimpl
    def create_cmd() -> None:
        """Create Jac CLI cmds."""

        @cmd_registry.register
        def studio() -> None:
            """Prepare jaseci studio"""
            from fastapi import FastAPI

            def get_graph(root: str):
                nodes = []
                edges = []

                edge_collection = NodeAnchor.Collection.get_collection("edge")
                node_collection = NodeAnchor.Collection.get_collection("node")
                node_docs = node_collection.find({"root": ObjectId(root)})
                edge_docs = edge_collection.find({"root": ObjectId(root)})

                for node in node_docs:
                    nodes.append(
                        {
                            "id": node["_id"],
                            "data": node["architype"],
                            "name": node["name"],
                        }
                    )
                for edge in edge_docs:
                    edges.append(
                        {
                            "id": edge["_id"],
                            "name": edge["name"],
                            "source": edge["source"],
                            "target": edge["target"],
                            "data": edge["architype"],
                        }
                    )

                return {
                    "nodes": json.loads(json.dumps(nodes, default=str)),
                    "edges": json.loads(json.dumps(edges, default=str)),
                }

            def get_users():
                users = []

                user_collection = NodeAnchor.Collection.get_collection("user")
                user_docs = user_collection.find()

                for user in user_docs:
                    users.append(
                        {
                            "id": user["_id"],
                            "root_id": user["root_id"],
                            "email": user["email"],
                        }
                    )

                return json.loads(json.dumps(users, default=str))

            app = FastAPI()
            app.add_middleware(
                CORSMiddleware,
                allow_origins=["*"],
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )

            app.add_api_route("/graph", endpoint=get_graph, methods=["GET"])
            app.add_api_route("/users", endpoint=get_users, methods=["GET"])
            client_dir = Path(__file__).resolve().parent.joinpath("client")
            print("dir", Path(__file__).resolve().parent.joinpath("client"))

            app.mount(
                "/",
                StaticFiles(directory=client_dir, html=True),
                name="studio",
            )

            app.mount(
                "/graph",
                StaticFiles(directory=client_dir, html=True),
                name="studio_graph",
            )

            run(app, host="0.0.0.0", port=8989)
