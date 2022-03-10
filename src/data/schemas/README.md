
<Item>Base
- contains fields common to all

<Item>
- inherits <Item>Base
- represents core entity from db table
- contains id
- replaces foreign key with parent object
- may contain list from many-to-many relationship if important
- mostly won't include children relationships (one to many)

<ItemAsModel>
- inherits <Item>Base
- is identical to <Item>, except it replaces parent object with foreign key

<ItemCreate>
- inherits <Item>Base
- does not contain id
- replaces foreign key with parent object

<ItemCreateAsModel>
- is identical to <ItemCreate>, except it replaces parent object with foreign key

<ItemDeep>
- inherits <Item>
- will contain all relationships, including children (one to many)
