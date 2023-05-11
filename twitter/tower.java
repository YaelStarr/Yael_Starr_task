import java.sql.SQLOutput;

public class tower {
    private int height;
    private int width;
    private boolean isRectangle;
    final int RIB_DIFFERENCE = 5;
    final int SIZE_LINE_BEFORE_THE_LAST = 3;

    public tower(int height, int width, boolean isRectangle) {
        this.height = height;
        this.width = width;
        this.isRectangle = isRectangle;
    }

    public String printRectangle() {
        if (height == width || Math.abs(height - width) > RIB_DIFFERENCE)
        {
            System.out.println("The area of the tower: " + height * width);
            return ("The area of the tower: " + height * width);
        }
        else {
            System.out.println("The perimeter of the tower: " + (height * 2 + width * 2));
            return ("The perimeter of the tower: " + (height * 2 + width * 2));
        }
    }

    public String printTriangularScope()
    {
        double rib = Math.sqrt(Math.pow(2, height) + Math.pow(2, width));
        return ("The perimeter of the tower: " + (rib*2 + width * 2));
    }

    public String printTriangularArea() {
        if (width % 2 == 0 || width > 2 * height) {
            System.out.println("The tower cannot be printed");
            return ("The tower cannot be printed");
        }
        else {
            String triangular = " ";
            for (int j = 0; j < width; j++)
                triangular += '*';
            triangular += '\n';
            int current_width = width;
            String current_line = " ";
            int block_size;
            try{block_size = (height - 2) / ((width - SIZE_LINE_BEFORE_THE_LAST)/2);}
            catch (Exception exception){block_size = 0;}
            int current_height = 1;
            for (int i = 0; i <= height; i++) {
                current_width -= 2;
                current_line = " ";
                for (int j = 0; j < width; j++) {
                    if (j < width / 2 - current_width / 2)
                        current_line += ' ';
                    else if (j < (width - current_width) / 2 + current_width)
                        current_line += '*';
                    else
                        current_line += ' ';
                }
                // if it's the last block
                int current_block_size = block_size;
                if ((i + 1) == block_size)
                    current_block_size += (height - 2) % ((width - SIZE_LINE_BEFORE_THE_LAST)/2);
                if (current_height!= height-1)
                    for (int j = 0; j < current_block_size; j++) {
                        triangular = current_line + '\n' + triangular;
                        current_height++;
                    }
                else {
                    triangular =  current_line + '\n' + triangular;
                    current_height++;
                    break;
                    }
            }
            System.out.println(triangular);
            return triangular;
        }
    }

    public void setHeight(int height) {
        this.height = height;
    }

    public void setWidth(int width) {
        this.width = width;
    }

    public void setRectangle(boolean rectangle) {
        isRectangle = rectangle;
    }

    public int getHeight() {
        return height;
    }

    public int getWidth() {
        return width;
    }

    public boolean isRectangle() {
        return isRectangle;
    }
}

