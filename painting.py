import numpy as np

fname = 'right_angle'
# fname = 'learn_and_teach'
# fname = 'logo'
input_file = fname + '.in'
output_file = fname + '.out'

# Read input
def read_input():
    wall = None
    with open(input_file) as f:
        lines = f.readlines()
        count = 0
        for line in lines:
            if (count == 0):
                num_rows = int(line.split()[0])
                num_cols = int(line.split()[1])
            else:
                if wall == None:
                    wall = [['.' for x in range(num_cols)] for x in range(num_rows)]
                wall[count - 1] = line[0:-1]
            count += 1
    return wall, num_rows, num_cols

# scan for lines (horizontal)
cells_cover_by_rows = 0
def scan_lines(wall):
    map_lines = dict()
    row_count = 0

    for (index, row) in enumerate(wall):
        list_lines = []
        # print row
        start_position = -1
        end_position = -1
        position = 0
        for cell in row:
            if start_position == -1 and cell == '#':
                start_position = position

            if ( ((position + 1 < len(row) and row[position + 1] == '.') or (position == len(row) - 1 and cell == '#') )
                and start_position != -1 and end_position == -1):
                end_position = position

            if start_position != -1 and end_position != -1:
                # found a line
                # print start_position, end_position
                list_lines.append( (start_position, end_position) )
                start_position = -1
                end_position = -1
                row_count += 1
                # cells_cover_by_rows += (end_position - start_position + 1)

            position += 1

        map_lines[index] = list_lines
    return row_count, map_lines

def scan_columns(wall):
    wall = [list(l) for l in wall]
    wall = np.array(wall)
    map_columns = dict()
    chunks_count = 0

    # Transpose wall to get the columns as rows
    for (idx_col, col) in enumerate(wall.transpose()):
        list_columns = []
        start_position = -1
        end_position = -1
        next_cell_not_painted = True
        for idx_row, cell in enumerate(col):
            has_start = start_position != -1
            has_end = end_position != -1

            current_cell_painted = cell == '#'

            next_not_outside_wall = idx_row + 1 < len(wall)
            if next_not_outside_wall:
                next_cell_not_painted = wall[idx_row+1, idx_col] == '.'
            in_last_row = idx_row == len(col) - 1

            is_last_in_chunck = (
                next_cell_not_painted or (in_last_row and current_cell_painted)
            )

            if not has_start and current_cell_painted:
                start_position = idx_row
                has_start=True

            if is_last_in_chunck and (has_start and not has_end):
                end_position = idx_row
                has_end = True

            if has_start and has_end:
                list_columns.append((start_position, end_position))
                start_position = -1
                end_position = -1
                chunks_count += 1

        map_columns[idx_col] = list_columns
    return chunks_count, map_columns


def search_rectangle(map_lines, num_rows, num_cols):
    # print map_lines
    left = 0
    right = num_cols - 1
    top = None
    bottom = num_rows - 1
    for row in range(num_rows):
        list_lines = map_lines.get(row, None)
        # print 'row'
        # print list_lines
        if list_lines:
            if top == None:
                top = row
            # list_lines_above = map_lines.get(row - 1, None)
            list_lines_below = map_lines.get(row + 1, None)
            first_line = list_lines[0]
            updated = False
            for (start_position, end_position) in list_lines_below:
                if start_position >= left and start_position <= right:
                    left = start_position
                    bottom = row + 1
                    updated = True
                    # print 'Update left'
                if end_position <= right and end_position >= left:
                    right = end_position
                    bottom = row + 1
                    updated = True
                    # print 'Update right'
                if start_position < left and right < end_position:
                    bottom = row + 1
                    updated = True
                    # return left, right, top, bottom
                # print 'start-end'
                # print start_position, end_position
                # print left, right, top, bottom
            if not updated:
                return left, right, top, bottom
    return left, right, top, bottom

def process_rectangle(map_lines, wall, l, r, t, b):
    # print 'process_rectangle'
    list_squares = []

    w = r - l + 1
    h = b - t + 1
    m = min(w, h)
    # print w, h

    if m < 3:
        # only need to draw at most 2 lines
        # if w < 3:
        # TODO put into map_lines
        clear_rectangle(l, r, t, b)
    else:
        if h > w:
            # size of square must be an odd number
            if w % 2 == 0:
                w -= 1
                r -= 1

            k = 1
            while t + w * k <= b:
                radius = (w - 1) / 2
                center = ( l + radius, t + radius + (k - 1) *w )
                list_squares.append( (radius, center) )
                k += 1

        elif h < w:
            # size of square must be an odd number
            if h % 2 == 0:
                h -= 1
                b -= 1

            k = 1
            while l + h * k <= r:
                radius = (h - 1) / 2
                center = ( l + radius + (k - 1) * h, t + radius )
                k += 1
                list_squares.append( (radius, center) )

        else:
            # this is a square
            # still need to adjust its size
            if w % 2 == 0:
                w -= 1

            radius = (w - 1) / 2
            center = ( l + radius, t + radius )
            list_squares.append( (radius, center) )

    # clear squares
    for square in list_squares:
        radius = square[0]
        center = square[1]
        print 'square ' + str(radius) + ', ' + str(center)
        clear_rectangle(center[0] - radius, center[0] + radius, center[1] - radius, center[1] + radius)

    return list_squares

def clear_rectangle(left, right, top, bottom):
    for row in range(top, bottom + 1):
        l = list(wall[row])
        for col in range(left, right + 1):
            l[col] = '.'
        wall[row] = "".join(l)

def generate_output_file_columns(map_cols, chunks):
    with open(output_file, 'w') as f:
        f.write(str(chunks) + '\n')
        for col in map_cols:
            for start, end in map_cols[col]:
                f.write('PAINT_LINE %d %d %d %d\n' % (start, col, end, col))

def generate_output_file(map_lines, row_count, num_rows):
    with open(output_file, 'w') as f:
        # print map_lines
        f.write(str(row_count) + '\n')
        for row in range(num_rows):
            list_lines = map_lines.get(row, None)
            if list_lines:
                for start_position, end_position in list_lines:
                    f.write('PAINT_LINE %d %d %d %d\n' % (row, start_position, row, end_position))


(wall, num_rows, num_cols) = read_input()
(chunks, map_columns) = scan_columns(wall)
generate_output_file_columns(map_columns, chunks)

# print 'row count', row_count
# print 'col count', col_count
# wall, num_rows = read_input()
# row_count, map_lines = scan_lines(wall)
# generate_output_file(map_lines, row_count, num_rows)

# wall, num_rows, num_cols = read_input()
# for i in range(100):
#     row_count, map_lines = scan_lines(wall)
#     rect = search_rectangle(map_lines, num_rows, num_cols)
#     # print rect
#     # print 'width', rect[1] - rect[0] + 1
#     # print 'height', rect[3] - rect[2] + 1
#     process_rectangle(map_lines, wall, *rect)
#     print
#     # clear_rectangle(*rect)
#     # for row in range(0, 10):
#     #     print wall[row][0:20]
#     # print
