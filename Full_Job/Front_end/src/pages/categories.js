import {category} from "../utils/keggMapsTable2Json"

export const Accordeon = (names) => {
  let finalKEggMapsArray = {
    "name":"br08901",
    "children":[]
  }
  for (let i = 0; i<names.length; i++){
    for(let j = 0; j<category.length; j++){
      if(names[i][1].includes(category[j].name)){
        if(finalKEggMapsArray.children.length === 0){
          finalKEggMapsArray.children.push({name:category[j].general_category, children:[]})
          finalKEggMapsArray.children[0].children.push({name:category[j].category, children:[]})
          finalKEggMapsArray.children[0].children[0].children.push({name:category[j].name, children:[]})
          finalKEggMapsArray.children[0].children[0].children[0].children.push({name:names[i]})
        }else{
          let checkGeneralCategory = finalKEggMapsArray.children.filter(order=>(order.name === category[j].general_category))
          if(checkGeneralCategory.length === 0){
            finalKEggMapsArray.children.push({name:category[j].general_category, children:[]})
            finalKEggMapsArray.children[finalKEggMapsArray.children.length-1].children.push({name:category[j].category, children:[]})
            finalKEggMapsArray.children[finalKEggMapsArray.children.length-1].children[0].children.push({name:category[j].name, children:[]})
            finalKEggMapsArray.children[finalKEggMapsArray.children.length-1].children[0].children[0].children.push({name:names[i]})
          }else{
            for(let k = 0; k<finalKEggMapsArray.children.length;k++){
              if(finalKEggMapsArray.children[k].name === category[j].general_category){
                let checkCategory = finalKEggMapsArray.children[k].children.filter(order => (order.name === category[j].category))
                if(checkCategory.length === 0){
                  finalKEggMapsArray.children[k].children.push({name:category[j].category, children:[]})
                  finalKEggMapsArray.children[k].children[finalKEggMapsArray.children[k].children.length-1].children.push({name:category[j].name, children:[]})
                  finalKEggMapsArray.children[k].children[finalKEggMapsArray.children[k].children.length-1].children[0].children.push({name:names[i]})

                }else{
                  for(let g = 0; g<finalKEggMapsArray.children[k].children.length; g++){
                    if(finalKEggMapsArray.children[k].children[g].name === category[j].category){
                      let checkName = finalKEggMapsArray.children[k].children[g].children.filter(order =>(order.name === category[j].name))
                      if(checkName.length === 0){
                        finalKEggMapsArray.children[k].children[g].children.push({name:category[j].name, children:[]})
                        finalKEggMapsArray.children[k].children[g].children[finalKEggMapsArray.children[k].children[g].children.length-1].children.push({name:names[i]})

                      }else{
                        for(let m = 0; m< finalKEggMapsArray.children[k].children[g].children.length;m++){
                          if(finalKEggMapsArray.children[k].children[g].children[m].name === category[j].name){
                            finalKEggMapsArray.children[k].children[g].children[m].children.push({name:names[i]})
                          }
                        }
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  }
  return(finalKEggMapsArray)
}