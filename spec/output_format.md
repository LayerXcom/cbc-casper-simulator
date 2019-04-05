```
- slot: 1  # global slot
  validators:  # validators in this network
  - current_slot: 1 # local slot (same with global slot for now)
    name: v0 # validator's name
    state: # validator's state of current_slot
      messages:
      - estimate:
          hash: 63943786622458  # block hash
          parent_hash: null  # parent block hash (null when genesis block)
        hash: 22809483422502  # message hash
        justification: []
        parent_hash: null  # parent message hash (null when genesis message)
        receiver_slot: 0  # receiver's slot when this message was received 
        sender: v0  # sender of this message
        sender_slot: 0  # sender's slot when this message was send
      - estimate:
          hash: 18436151933990
          parent_hash: 63943786622458
        hash: 29588784803832
        justification:
        - message_hash: 22809483422502
          sender: v0
        parent_hash: 22809483422502
        receiver_slot: 0
        sender: v0
        sender_slot: 0
        ...
```