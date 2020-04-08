import random

N_PROCESSORS = 7

class MockRegionAddresses(object):
    def __init__(self):
        self.n_pairs = random.randint(1, N_PROCESSORS-3)
        self.n_filters = list()
        for i in range(self.n_pairs):
            self.n_filters.append(random.randint(1, 10))

class CBHostBasedBitFieldRouterCompressor(object):

    def __init__(self):
        # small variables in DTCM
        self._core_neurons = [0] * N_PROCESSORS
        self.processor_heads = [None] * N_PROCESSORS

        # variable declarations for things to be malloced
        self._bit_fields = None
        self._n_redundant_packets = None
        self._processor_ids = None
        self._sort_order = None

    def _swap_lists(self, one, two):
        # Assumption is processor_ids are the same and sort_order unused
        temp = self._n_redundant_packets[one]
        self._n_redundant_packets[one] = self._n_redundant_packets[two]
        self._n_redundant_packets[two] = temp
        temp = self._bit_fields[one]
        self._bit_fields[one] = self._bit_fields[two]
        self._bit_fields[two] = temp

    def _swap_lists2(self, one, two):
        self._swap_lists(one, two)
        temp = self._processor_ids[one]
        self._processor_ids[one] = self._processor_ids[two]
        self._processor_ids[two] = temp
        temp = self._sort_order[one]
        self._sort_order[one] = self._sort_order[two]
        self._sort_order[two] = temp

    def _sort_by_redundant_packet(self, sort_start, sort_end):
        """
        Sort bitfields and n_reducnat_packets for a zone with all the
            same processor_id

        Just use a Bubble sort to avoid recurrsion
        """
        for i in range(sort_start, sort_end -1):
            for j in range(i+1, sort_end):
                if self._n_redundant_packets[i] < self._n_redundant_packets[j]:
                    self._swap_lists(i, j)

    def print(self):
        print(self.n_bit_fields)
        print(self._bit_fields)
        print(self._n_redundant_packets)
        print(self._processor_ids)
        print(self._sort_order)
        print(self._core_neurons)
        print(self.processor_heads)
        print("--")

    def read_in_bit_fields(self):
        region_address = MockRegionAddresses()
        n_pairs_of_addresses =  region_address.n_pairs

        # Caulculate n_bit_fields
        self.n_bit_fields = 0
        for r_id in range( n_pairs_of_addresses):
            self.n_bit_fields += region_address.n_filters[r_id]

        # Malloc the arrays
        self._bit_fields = [None] * self.n_bit_fields
        self._n_redundant_packets = [None] * self.n_bit_fields
        self._processor_ids = [None] * self.n_bit_fields
        self._sort_order = [None] * self.n_bit_fields

        # Read in the data
        index = 0
        for r_id in range(n_pairs_of_addresses):
            # lets not start the processors numbers at 0
            processor_id = r_id + 3

            sort_start = index
            for bf_id in range(region_address.n_filters[r_id]):
                # lets not start the processors numbers at 0
                self._processor_ids[index] = processor_id

                # Just use index as bitfeild to track sorting
                self._bit_fields[index] = index

                # Get n_atoms from region_addresses_t.key_atom
                n_atoms = random.randint(1, 10)
                self._core_neurons[processor_id] += n_atoms
                # Calc n_redundant_packets based on bit_field and n_atoms
                self._n_redundant_packets[index] = random.randint(0, n_atoms)
                index+= 1
            self._sort_by_redundant_packet(sort_start, index)

    def _sort_by_order(self):
        """
        Sorts the list based on the index in sort_order list.

        Everytime there is a swap at least one of the rows is moved to the
            final place.
        There is one check per row in the for loop plus if the first fails
            up to one more for each row about to be moved to the correct place.
        :return:
        """
        # Check each row in the lists
        for i in range(self.n_bit_fields):
            # check that the data is in the correct place
            while self._sort_order[i] != i:
                # If not swap the data there into the correct place
                self._swap_lists2(i, self._sort_order[i])

    def order_bit_fields(self):
        self.processor_heads = list()
        for i in range(N_PROCESSORS):
            self.processor_heads.append(None)
        last_processor = -1
        for i in range(len(self._processor_ids)):
            if self._processor_ids[i] != last_processor:
                self.processor_heads[self._processor_ids[i]] = i
                last_processor = self._processor_ids[i]
        for i in range(len(self._processor_ids)):
            worst_core = 0
            highest_neurons = -1
            for c in range(N_PROCESSORS):
                print(c)
                print(self._core_neurons)
                if self._core_neurons[c] > highest_neurons:
                    worst_core = c
                    highest_neurons = self._core_neurons[c]
            # print(worst_core)
            index = self.processor_heads[worst_core]
            self._sort_order[index] = i
            if (self.processor_heads[worst_core] + 1 < len(
                    self._processor_ids) and
                    self._processor_ids[self.processor_heads[worst_core]] ==
                    self._processor_ids[self.processor_heads[worst_core] + 1]):
                self._core_neurons[worst_core] -= self._n_redundant_packets[
                    index]
                self.processor_heads[worst_core] += 1
            else:
                self.processor_heads[worst_core] = -1
                self._core_neurons[worst_core] = -1
        self._sort_by_order()

if __name__ == '__main__':
    cb = CBHostBasedBitFieldRouterCompressor()
    cb.read_in_bit_fields()
    cb.print()
    cb.order_bit_fields()
    cb.print()