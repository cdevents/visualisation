from arango import ArangoClient
from arango import exceptions
import json
import os
 

class Arangoclientquery:
    def __init__(self):
        self.setup()

    def setup(self):
        # Initialize the ArangoDB client.
        arangohome = os.environ.get('ARANGOHOME', 'http://localhost:8529')
        client = ArangoClient(hosts=arangohome)

        # Connect to "_system" database as root user.
        # This returns an API wrapper for "_system" database.
        sys_db = client.db('_system', username='root', password='passwd')

        # List all databases.
        sys_db.databases()

        # Create a new database named "test" if it does not exist.
        # Only root user has access to it at time of its creation.
        if not sys_db.has_database('test'):
            sys_db.create_database('test')


        db = client.db('test', username='root', password='passwd')

        # List existing graphs in the database.
        # db.graphs()

        # Create a new graph named "school" if it does not already exist.
        # This returns an API wrapper for "school" graph.
        if db.has_graph('CDEvents'):
            
            self.cdevents = db.graph('CDEvents')
        else:
            self.cdevents = db.create_graph('CDEvents')
        
        print(self.cdevents)
        
        # Get the API wrapper for graph "school".
        #cdevents = db.graph('CDEvents')

        # Create a new vertex collection named "lectures" if it does not exist.
        # This returns an API wrapper for "lectures" vertex collection.
        if self.cdevents.has_vertex_collection('cdevent'):
            cdevent = self.cdevents.vertex_collection('cdevent')
        else:
            cdevent = self.cdevents.create_vertex_collection('cdevent')

        # Get the API wrapper for edge collection "teach".
        if self.cdevents.has_edge_definition('links'):
            self.links = self.cdevents.edge_collection('links')
        else:
            self.links = self.cdevents.create_edge_definition(
                edge_collection='links',
                from_vertex_collections=['cdevent'],
                to_vertex_collections=['cdevent']
            )

    def getNodes(self,id):
        # List edges going in/out of a vertex.
        #print(links.edges('cdevent/event3', direction='in'))
        #print(links.edges('cdevent/event3'))
        #print(links.edges('cdevent/event1'))
        #print(links.edges('cdevent/event7'))
        result = {}
        # Traverse the graph in outbound direction, breath-first.
        try:
            result = self.cdevents.traverse(
            start_vertex='cdevent/'+str(id),
            direction='any'
            #strategy='bfs',
            #edge_uniqueness='global',
            #vertex_uniqueness='global',
            )
        except Exception as err:
            print('Handling run-time error:', err)

        
        print(result)

        return result
    

