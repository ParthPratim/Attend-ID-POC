import hashlib
import cbor
import logging
from processor.state import StateHelper

ACTION_CREATE_NEW_ORG = "CREATE_NEW_ORG"
ACTION_ADD_NEW_ORG_MEMBER = "ADD_NEW_ORG_MEMBER"
ACTION_TRANSFER_ORG_MEMBER = "TRANSFER_ORG_MEMBER"
ACTION_BUILD_FR_MODEL = "BUILD_FR_MODEL"

class TransactionHandler:
    def __init__(self,tx_payload,context=None):
        self._tx_payload = tx_payload
        self._context = context
    def process(self):
        print("CALLED PROC...1")
        if self._tx_payload.action == ACTION_CREATE_NEW_ORG:
            print("CALLED PROC...")
            state_addr = StateHelper(self._tx_payload.org_id,self._tx_payload.creator_id).state_address
            state_data = {
                'Organization' : self._tx_payload.org_name,
                'CreatorID' : self._tx_payload.creator_id,
                'OrgID' : self._tx_payload.org_id,
                'MemberCount' : 0,
                'FRModel' : "",
                "CertificateHash" : self._tx_payload.certificate_hash,
                "BDB_pub_key" : self._tx_payload.bdb_keys[0],
                "BDB_priv_key" : self._tx_payload.bdb_keys[1]
            }
            formatted_data = TransactionHandler.serialize(state_data)
            print(formatted_data)
            print(state_addr)
            self._context.set_state(
                {
                    state_addr : formatted_data
                },
                timeout=3
            )
            print("Added New Org")

        elif self._tx_payload.action == ACTION_ADD_NEW_ORG_MEMBER:
            state_addr = StateHelper(self._tx_payload.org_id,self._tx_payload.creator_id).state_address
            state_entries = self._context.get_state(
                [state_addr],
                timeout=3
            )
            if state_entries == []:
                print("BAD ORGANIZATION REFERENCE")
            else:
                state_data = TransactionHandler.deserialize(state_entries[0].data)
                state_data['MemberCount'] = state_data['MemberCount'] + 1
                formatted_data = TransactionHandler.serialize(state_data)
                self._context.set_state(
                    {
                        state_addr : formatted_data
                    },
                    timeout=3
                )
                base = hashlib.sha512("digital_id".encode('utf-8')).hexdigest()[0:6]
                creator_id_hash = hashlib.sha512(self._tx_payload.new_member_id.encode('utf-8')).hexdigest()[-64:]
                did_addr = base+creator_id_hash
                state_entries = self._context.get_state(
                    [did_addr],
                    timeout=3
                )
                if state_entries == []:
                    print("Invalid Digital ID")
                else:
                    state_data = TransactionHandler.deserialize(state_entries[0].data)
                    state_data['Organizations'].append(self._tx_payload.org_id)
                    print(self._tx_payload.can_mark_attendance)
                    if self._tx_payload.can_mark_attendance == "True":
                        print("CanMarkAttendance")
                        state_data['CanMarkAttendance'] = True
                    formatted_data = TransactionHandler.serialize(state_data)
                    self._context.set_state(
                        {
                            did_addr : formatted_data
                        },
                        timeout=3
                    )
        elif self._tx_payload.action == ACTION_TRANSFER_ORG_MEMBER:
            state_addr = StateHelper(self._tx_payload.org_id,self._tx_payload.creator_id).state_address
            state_addr2 = StateHelper(self._tx_payload.new_org_id,self._tx_payload.new_org_creator).state_address
            state_entries = self._context.get_state(
                [state_addr,state_addr2],
                timeout=3
            )
            if state_entries == []:
                print("BAD ORGANIZATION REFERENCE")
            else:
                state_data = TransactionHandler.deserialize(state_entries[0].data)
                state_data['MemberCount'] = state_data['MemberCount'] - 1
                state_data2 = TransactionHandler.deserialize(state_entries[1].data)
                state_data2['MemberCount'] = state_data['MemberCount'] + 1
                formatted_data = TransactionHandler.serialize(state_data)
                formatted_data2 = TransactionHandler.serialize(state_data2)
                self._context.set_state(
                    {
                        state_addr : formatted_data,
                        state_addr2 : formatted_data2
                    },
                    timeout=3
                )
                base = hashlib.sha512("digital_id".encode('utf-8')).hexdigest()[0:6]
                creator_id_hash = hashlib.sha512(self._tx_payload.curr_member_id.encode('utf-8')).hexdigest()[-64:]
                did_addr = base+creator_id_hash
                state_entries = self._context.get_state(
                    [did_addr],
                    timeout=3
                )
                if state_entries == []:
                    print("Invalid Digital ID")
                else:
                    state_data = TransactionHandler.deserialize(state_entries[0].data)
                    state_data['Organizations'].remove(self._tx_payload.org_id)
                    state_data['Organizations'].append(self._tx_payload.new_org_id)
                    formatted_data = TransactionHandler.serialize(state_data)
                    self._context.set_state(
                        {
                            did_addr : formatted_data
                        },
                        timeout=3
                    )

        elif self._tx_payload.action == ACTION_BUILD_FR_MODEL:
            state_addr = StateHelper(self._tx_payload.org_id,self._tx_payload.creator_id).state_address
            state_entries = self._context.get_state(
                [state_addr],
                timeout=3
            )
            if state_entries == []:
                print("Invalid ORG REFERENCE")
            else:
                state_data = TransactionHandler.deserialize(state_entries[0].data)
                state_data['FRModel'] = self._tx_payload.frmodel
                formatted_data = TransactionHandler.serialize(state_data)
                self._context.set_state(
                    {
                        state_addr : formatted_data,
                    },
                    timeout=3
                )


    @staticmethod
    def serialize(org_data):
        return cbor.dumps(org_data)

    @staticmethod
    def deserialize(cbor_data):
        return cbor.loads(cbor_data)
