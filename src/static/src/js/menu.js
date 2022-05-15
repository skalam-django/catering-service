import {MDCSelect} from '@material/select';
import {MDCTextField} from '@material/textfield';
import {MDCList} from "@material/list";
import {MDCRipple} from '@material/ripple';
import {MDCFormField} from '@material/form-field';
import {MDCCheckbox} from '@material/checkbox';
import {MDCTextFieldIcon} from '@material/textfield/icon';
import {BASE_JS} from "../../../../catering_service/static/catering_service/js/base"
import {Layout1} from "../../../../catering_service/static/catering_service/js/layout_1"


const Menu = (function() {
  let menu_pdf_textfield = undefined; 
  let selected_pdf_ids = new Array();
  function menu_pdf_fn(){}; 


  BASE_JS.docReady(function(event) {
    const select_el = document.querySelector('.mdc-select')
    const select = new MDCSelect(select_el);
    console.log("select: ", select);
    let idx = BASE_JS.getUrlParameter('idx');
    if(idx!=undefined && idx!=null){
      console.log("idx: ", idx);
      select.setValue(idx);
    }
    select.listen('MDCSelect:change', () => {
      window.location.href = `/?idx=${select.value}`;

    });
  
    const pdf_form_field = document.querySelector('.mdc-form-field');
    let formField = undefined;
    if(pdf_form_field!=undefined && pdf_form_field!=null){
      formField = new MDCFormField(pdf_form_field);
    }    
    const pdf_checkboxs = document.querySelectorAll('.mdc-checkbox');
    if(pdf_checkboxs!=undefined && pdf_checkboxs!=null){
      pdf_checkboxs.forEach(
        function(pdf_checkbox, x, z){
          if(pdf_checkbox!=undefined && pdf_checkbox!=null){
            const checkbox = new MDCCheckbox(pdf_checkbox);
            checkbox.listen('change', (event) => {
              var id = event.srcElement.id.replace('checkbox-', '');
              if (event.target.checked){
                if (selected_pdf_ids.includes(id)==false){
                 selected_pdf_ids.push(id); 
                }
              }else{
                if (selected_pdf_ids.includes(id)==true){
                 selected_pdf_ids = selected_pdf_ids.filter(item => item !== id)
                }
              }
              var ids = "";
              if (selected_pdf_ids.length>0){
                ids = selected_pdf_ids.join();
              }
              document.querySelector('#id_ids').value = ids;
              console.log("selected_pdf_ids: ", selected_pdf_ids)
            })
            formField.input = checkbox;
            for(var id in menu_pdfs){
              var pdf_rel_path = menu_pdfs[id];
              var lbl_el = document.querySelector(`#lbl-${id.split('pdf-')[1]}`);
              if(lbl_el!=null){
                lbl_el.textContent = pdf_rel_path.split('/')[1];
              }
              PDFObject.embed(`/${pdf_rel_path}`, `#${id}`, {page: "1"});
            }
          }
        }
      )
    }
    

    let share_btn = new Layout1.ShareBtn();
    share_btn.open(
      function(){
        let dialog = new BASE_JS.ShareDialog(
          'Menu PDF | Niraj Caterer',
          {'method': 'post'},
          // {},
          undefined,
          {text : 'SHARE', type : 'submit'},
          // {text : 'ADD'},
          {text : 'CANCEL'},
          function(evt){
            console.info("Dialog opened", evt);
            var list = new MDCList(document.querySelector('#share-dialog .mdc-list'));
            var listItemRipples = list.listElements.map((listItemEl) => new MDCRipple(listItemEl));
            var alltextfield_el = document.querySelectorAll('#share-dialog .mdc-text-field');
            try{
              for(var i=0; i<alltextfield_el.length; i++){
                var textfield_el = alltextfield_el[i];
                var textField = new MDCTextField(textfield_el);
            
              }
            }catch(e){
              console.error("Error1 : ", e);
            }

            try{
              var alltextfield_icon = document.querySelectorAll('#share-dialog .mdc-text-field__icon');
              for(var j=0; j<alltextfield_icon.length; j++){
                var textfield_icon = alltextfield_icon[j];
                try{
                  var icon = new MDCTextFieldIcon(textfield_icon);
                }catch(e){
                  console.error("Error3 : ", e);
                }
              }
            }catch(e){
              console.error("Error4 : ", e);
            }
          }, 
          function(evt){
            console.info("Dialog closed", evt);
          });
        if(selected_pdf_ids.length>0){
          dialog.open();
        }else{
          var snackbar = new BASE_JS.SnackBar('Please select at least one menu pdf to share.');
          snackbar.open();
        }
    })


    let fab_btn = new Layout1.FabBtn('Add Menu');
    fab_btn.open(
      function(){
        let dialog = new BASE_JS.FabDialog(
          'Add Menu',
          {'method': 'post'},
          // {},
          undefined,
          {text : 'ADD', type : 'submit'},
          // {text : 'ADD'},
          {text : 'CANCEL'},
          function(evt){
            console.info("Dialog opened", evt);
            var list = new MDCList(document.querySelector('#fab-dialog .mdc-list'));
            var listItemRipples = list.listElements.map((listItemEl) => new MDCRipple(listItemEl));
            var alltextfield_el = document.querySelectorAll('#fab-dialog .mdc-text-field');
            try{
              for(var i=0; i<alltextfield_el.length; i++){
                var textfield_el = alltextfield_el[i];
                var textField = new MDCTextField(textfield_el);
                var menu_pdf = textfield_el.querySelector('[name="menu_pdf"]');
                try{
                  if (menu_pdf!=undefined){
                    menu_pdf_textfield = textField;
                    menu_pdf_fn = function(){menu_pdf.click()};
                    menu_pdf.onchange = function(){
                      // console.info('file name: ', menu_pdf.files[0].name);
                      textField.value = menu_pdf.files[0].name;
                    };
                    textField.listen('click', menu_pdf_fn);
                  }
                }catch(e){
                  console.error("Error1 : ", e);
                }
              }
            }catch(e){
              console.error("Error2 : ", e);
            }

            try{
              var alltextfield_icon = document.querySelectorAll('#fab-dialog .mdc-text-field__icon');
              for(var j=0; j<alltextfield_icon.length; j++){
                var textfield_icon = alltextfield_icon[j];
                try{
                  var icon = new MDCTextFieldIcon(textfield_icon);
                }catch(e){
                  console.error("Error3 : ", e);
                }
              }
            }catch(e){
              console.error("Error4 : ", e);
            }
          }, 
          function(evt){
            console.info("Dialog closed", evt);
            try{
              menu_pdf_textfield.unlisten('click', menu_pdf_fn);
            }catch(e){
              console.error("Error5 : ", e);
            }
          });
        dialog.open();
    })
  });
})()

