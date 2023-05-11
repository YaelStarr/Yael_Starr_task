
//package project;

import java.net.URL;
import java.util.ArrayList;
import java.util.ResourceBundle;

import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.TextArea;
import javafx.scene.control.TextField;

public class ProjectController {

    tower current_tower;
    @FXML
    private ResourceBundle resources;

    @FXML
    private URL location;

    @FXML
    private Button btnPrint;

    @FXML
    private Button btnPrintTriangle;

    @FXML
    private Button btnRectangle;

    @FXML
    private Button btnTriangleParameter;

    @FXML
    private Button btnTriangular;

    @FXML
    private Label lblHeight;

    @FXML
    private Label lblMain;

    @FXML
    private Label lblWidth;

    @FXML
    private TextField txtHeight;

    @FXML
    private TextField txtWidth;

    @FXML
    private TextArea txtArea;


    @FXML
    void printClicked(ActionEvent event) {
        try {
            current_tower.setHeight(Integer.parseInt(txtHeight.getText()));
            current_tower.setWidth(Integer.parseInt(txtWidth.getText()));
        }
        catch (Exception e)
        {
            System.out.println("Only Integers numbers are allowed");
            current_tower.setHeight(0);
            current_tower.setWidth(0);
        }
        btnPrint.setVisible(false);
        if (current_tower.isRectangle())
        {
            txtArea.setText(current_tower.printRectangle());
            buildingTower();
        }
        else
        {
            lblHeight.setVisible(false);
            lblWidth.setVisible(false);
            txtHeight.setVisible(false);
            txtWidth.setVisible(false);
            btnPrintTriangle.setVisible(true);
            btnTriangleParameter.setVisible(true);
        }
    }

    @FXML
    void rectangleSelected(ActionEvent event) {
        current_tower.setRectangle(true);
        lblMain.setText("RECTANGLE TOWER");
        btnTriangular.setVisible(false);
        btnRectangle.setVisible(false);
        allowDataEntry();

    }

    @FXML
    void triangularSelected(ActionEvent event) {
        current_tower.setRectangle(false);
        lblMain.setText("TRIANGULAR TOWER");
        btnTriangular.setVisible(false);
        btnRectangle.setVisible(false);
        allowDataEntry();
    }



    @FXML
    void printTriangle(ActionEvent event) {
        txtArea.setText(current_tower.printTriangularArea());
        buildingTower();
    }

    @FXML
    void printTriangleParameter(ActionEvent event) {
        txtArea.setText(current_tower.printTriangularScope());
        buildingTower();
    }

    @FXML
    void initialize() {
        assert btnPrint != null : "fx:id=\"btnPrint\" was not injected: check your FXML file 'project.fxml'.";
        assert btnPrintTriangle != null : "fx:id=\"btnPrintTriangle\" was not injected: check your FXML file 'project.fxml'.";
        assert btnRectangle != null : "fx:id=\"btnRectangle\" was not injected: check your FXML file 'project.fxml'.";
        assert btnTriangleParameter != null : "fx:id=\"btnTriangleParameter\" was not injected: check your FXML file 'project.fxml'.";
        assert btnTriangular != null : "fx:id=\"btnTriangular\" was not injected: check your FXML file 'project.fxml'.";
        assert lblHeight != null : "fx:id=\"lblHeight\" was not injected: check your FXML file 'project.fxml'.";
        assert lblMain != null : "fx:id=\"lblMain\" was not injected: check your FXML file 'project.fxml'.";
        assert lblWidth != null : "fx:id=\"lblWidth\" was not injected: check your FXML file 'project.fxml'.";
        assert txtHeight != null : "fx:id=\"txtHeight\" was not injected: check your FXML file 'project.fxml'.";
        assert txtWidth != null : "fx:id=\"txtWidth\" was not injected: check your FXML file 'project.fxml'.";
        current_tower = new tower(0, 0, false);
        buildingTower();

    }

    public void buildingTower()
    {
        btnRectangle.setVisible(true);
        btnTriangular.setVisible(true);
        btnPrint.setVisible(false);
        lblHeight.setVisible(false);
        lblWidth.setVisible(false);
        txtHeight.setVisible(false);
        txtWidth.setVisible(false);
        btnPrintTriangle.setVisible(false);
        btnTriangleParameter.setVisible(false);
        lblMain.setText("twitter");
    }

    public void allowDataEntry()
    {
        lblHeight.setVisible(true);
        lblWidth.setVisible(true);
        txtHeight.setVisible(true);
        txtWidth.setVisible(true);
        txtHeight.setText("");
        txtWidth.setText("");
        btnPrint.setVisible(true);
    }


}










