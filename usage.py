import converter

m=converter.message(packet='0100c8110000d307000002')
print(m.unpack_packet())
print(m.pack_packet({'packet_type': 1, 'packet_version': 0, 'total_energy_used_watt_hour': 4552, 'time_drift_milli_seconds': 2003, 'flags': 0}))


