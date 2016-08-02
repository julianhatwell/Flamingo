# create team membership
MATCH (v:User)-[r:CreateChat]->(:ChatItem)-[o:PartOf]->(:TeamChatSession)-[b:OwnedBy]->(w:Team)
WITH DISTINCT v, w
CREATE (v)-[:MemberOf]->(w)

MATCH (v:User)-[m:MemberOf]->(w:Team)
RETURN m LIMIT 25
