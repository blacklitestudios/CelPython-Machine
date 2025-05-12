def apply_to_cells(self, priority, func: callable):
    '''Gets all the cells with a given ID and a direction, and orders them for sub-sub-ticking.'''
    a: range
    b: range
    match priority:

                        case "rightdown":
                            a = range(self.grid_width)
                            b = range(self.grid_height)
                        case "rightup":
                            a = range(self.grid_width)
                            b = reversed(range(self.grid_height))

                        case "leftdown":
                            a = reversed(range(self.grid_width))
                            b = range(self.grid_height)
                        case "leftup":
                            a = reversed(range(self.grid_width))
                            b = reversed(range(self.grid_height))


                        case "downright":
                            a = range(self.grid_height)
                            b = range(self.grid_width)
                        case "downleft":
                            a = range(self.grid_height)
                            b = reversed(range(self.grid_width))

                        case "upright":
                            a = reversed(range(self.grid_height))
                            b = range(self.grid_width)
                        case "upleft":
                            a = reversed(range(self.grid_height))
                            b = reversed(range(self.grid_width))

    
    result = []
    for i in b:
        for j in a:
            
            result.append(((i, j) if priority[0] in ["d", "u"] else (j, i)))
    return result
    