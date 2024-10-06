import p4runtime_sh.p4runtime as p4sh_rt
import p4runtime_sh.shell as p4sh
import logging
from utils import disable_print, enable_print


def init_shell():
    p4sh.setup(
        device_id=0,
        grpc_addr='127.0.0.1:9559',
        election_id=(0, 1),
    )


def insert_underlay_entry(entry, match: str, action: str, next_hop_id: str):
    try:
        logging.info(f"Inserting underlay entry: {match} -> (Action:{action}, NextHopId: {next_hop_id})")

        disable_print()
        entry.match["meta.dst_ip_addr"] = match
        entry.action["packet_action"] = action
        entry.action["next_hop_id"] = next_hop_id
        entry.insert()
    except p4sh_rt.P4RuntimeWriteException as e:
        logging.error(f"Failed to insert underlay entry: {e}")
    finally:
        enable_print()


def init_underlay():
    logging.info("Inserting underlay entries ...")

    underlay_entry = p4sh.TableEntry("dash_ingress.underlay.underlay_routing")(action="dash_ingress.underlay.pkt_act")
    insert_underlay_entry(underlay_entry, "::10.0.0.37/128", action="1", next_hop_id="0")
    insert_underlay_entry(underlay_entry, "::10.0.0.39/128", action="1", next_hop_id="2")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    # sh.global_options["verbose"] = False

    init_shell()
    init_underlay()
