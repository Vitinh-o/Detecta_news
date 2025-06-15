//Pega os elemntos selecionados pelo usuário
const pelo_link = document.getElementById("botao_pelo_link")
const pelo_texto = document.getElementById("botao_pelo_texto")
const por_imagem = document.getElementById("botao_por_imagem")

//Pega os botões que enviam as informações para o servidor
const enviar = document.getElementById("enviar_para_pesquisa")
const enviar_IA = document.getElementById("enviar_IA")

//Pega os botões que trocam o campo para enviar as informações
const controla_css_input_texto = document.getElementById("conteudo_texto")
const controla_css_input_link = document.getElementById("conteudo_link")
const controla_css_input_imagem = document.getElementById("conteudo_imagem")

//Verifica em qual item o usuário está (A tela abre inicialmente na opção por texto)
let texto_link_imagem = "conteudo_texto"

//Pega o elemento que exibirá a resposta da IA
var resposta = document.getElementById("resposta_ia")

//Pega o elemento sppiner
const carregar = document.getElementById('carregar')


const previewImagem = document.getElementById("preview_imagem");
const mostrar_texto_ia = document.getElementById('mostar_texto_ia')
const texto_ia = document.getElementById("texto_ia")
const url = 'http://127.0.0.1:8000'
const imagem_default = 'imagens/imagem_padrao.jpg'
const carregando_texto = "Carregando"
const mensagem = "Encontramos algumas notícias já verificadas que parecem estar relacionadas à sua. Você ainda deseja enviar para a IA verificar a notícia?"
const resultsContainer = document.getElementById("noticias_encontradas");

//Controla a visualização dos elementos que o usuário pode enviar a notícia
function mudar_elementos(input) {
    limpa_tela()
    controla_css_input_texto.style.display = input === 'conteudo_texto' ? 'block' : 'none';
    controla_css_input_link.style.display = input === 'conteudo_link' ? 'block' : 'none';
    controla_css_input_imagem.style.display = input === 'conteudo_imagem' ? 'block' : 'none';
    texto_link_imagem = input;
    resultsContainer.innerText = ""
    previewImagem.style.display = "none";
    
    var textarea = document.getElementById("conteudo_texto")
    textarea.value = "";

    var conteudoimg = document.getElementById("conteudo_imagem")
    conteudoimg.value = "";

    var conteudolink = document.getElementById("conteudo_link")
    conteudolink.value = "";

}
pelo_link.addEventListener("click", () => mudar_elementos('conteudo_link'));
pelo_texto.addEventListener("click", () => mudar_elementos('conteudo_texto'));
por_imagem.addEventListener("click", () => mudar_elementos('conteudo_imagem'));

//Limpa a tela retornando o css ao estadado inicial
function limpa_tela(){

        mostrar_texto_ia.style.display = "none"
        texto_ia.innerText = mensagem
        resposta.innerText = ""
        
}

//Busca os dados e cria o HTML para mostar as notícas encontradas relacionadas ao que o usuário inseriu
function mostra_noticias_encontradas(data){
    
    resposta.innerText = ""
    resultsContainer.innerHTML = " ";

    //Verifica se o retorno do Data é do tipo array
    if (Array.isArray(data)) {
        
        //Verifica se existe notícias e caso não muda a mensagem 
        if (data.length === 0)
            texto_ia.innerText = "Não encontramos essa notícia em sites de verificação. Deseja prosseguir enviando-a para análise pela IA?"

        mostrar_texto_ia.style.display = "block"

        //Cria os cards no HTML 
        container = " "
        data.forEach(item => {

            const link = item.link;
            const title = item.title;
            const image = item.image || 'imagens/imagem_padrao.jpg';  // Imagem ou padrão

            container += `
                <div class="col-md-3">
                    <div class="card mb-2" style="width: 17rem;">
                        <img src="${image}" class="card-img-top" alt="${title}" style="height: 200px; object-fit: cover;">
                        <div class="card-body">
                            <h5 class="card-title">${title}</h5>
                            <a href="${link}" target="_blank" class="btn btn-primary">Leia mais</a>
                        </div>
                    </div>
                </div>`;
        });

        container += `</div></div>`;
        resultsContainer.innerHTML += container;



    }
    //Caso o tipo retornado seja uma String ele adiciona a mensagem abaixo
    else
        resultsContainer.innerHTML = "<h6>" + data + "</h6>"
}


enviar.addEventListener("click", function() {

    enviar_IA.style.display = 'block'
    enviar_IA.style.margin = '0 auto'

    //Pega qual visualização o usuário está
    tag = document.getElementById(texto_link_imagem);

    //Verifica se o usuário inseriu informações nos campos e caso não não realiza nenhuma ação
    if (tag.value === "") return undefined;

    //Inicia o spinner
    carregar.style.display = 'flex'

    //Limpa a tela retornando o css ao estadado inicial
    limpa_tela()

    //Pega a visualização que o usuário está no momento
    let requisicao_final = tag.value;

    //Envia o conteúdo inserido para o usuário verificando em qual visualização ele está no momento
    if(texto_link_imagem == "conteudo_link"){
        link_texto = `${url}/notice_text_form?recived_link=${encodeURIComponent(requisicao_final)}`

        fetch(link_texto, {
        method: 'GET',
        mode: 'cors',
        headers: {
            'Content-Type': 'application/json',
        },        
        })
        .then(response => {
            if (!response.ok) {
                carregar.style.display = 'none'
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        //Resposta do servidor para quando o usário envia texto ou link
        .then(data => {
            carregar.style.display = "none"
            mostra_noticias_encontradas(data)
        
        })
        .catch(error => console.error('Erro:', error));  // Tratamento de erros
    }

    else if (texto_link_imagem == "conteudo_texto"){
        link_texto = `${url}/notice_text_form?text_notice=${encodeURIComponent(requisicao_final)}`
    
        fetch(link_texto, {
        method: 'GET',
        mode: 'cors',
        headers: {
            'Content-Type': 'application/json',
        },        
        })
        .then(response => {
            if (!response.ok) {
                carregar.style.display = 'none'
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        //Resposta do servidor para quando o usário envia texto ou link
        .then(data => {
            carregar.style.display = "none"
            mostra_noticias_encontradas(data)
        
        })
        .catch(error => console.error('Erro:', error));  // Tratamento de erros
    }
    
    else{

        //Pega a imagem que o usuário inseriu
        let arquivo = controla_css_input_imagem.files[0]

        //Formata imagem
        let formData = new FormData();
        formData.append('image', arquivo);

        //Envia a imagem via post para o servidor
        fetch('http://127.0.0.1:8000/notice_image', {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        //Resposta do servidor para quando o usário envia a imagem
        .then(data => {   
            carregar.style.display = "none"
            mostra_noticias_encontradas(data)  
        })
        .catch(error => {
            console.error('Erro:', error);
        });
    }
    
});


enviar_IA.addEventListener("click", function() {

    //Pega qual visualização o usuário está
    tag = document.getElementById(texto_link_imagem);

    //Verifica se o usuário inseriu informações nos campos e caso não não realiza nenhuma ação
    if (tag.value === "") return undefined;

    //Mostra o loading
    carregar.style.display = 'flex'

    //Pega os dados que o usuário inseriu
    let requisicao_final = tag.value;

    //Envia o conteúdo inserido para o usuário verificando em qual visualização ele está no momento
    if(texto_link_imagem == "conteudo_link")
        
        link_texto = `http://127.0.0.1:8000/notice?recived_link=${encodeURIComponent(requisicao_final)}`

    else if (texto_link_imagem == "conteudo_texto"){
        link_texto = `http://127.0.0.1:8000/notice?text_notice=${encodeURIComponent(requisicao_final)}`
    }
    else{
        link_texto = `http://127.0.0.1:8000/notice?recived_image=${encodeURIComponent("imagem")}`
    }

    fetch(link_texto, {
        method: 'GET',
        mode: 'cors',
        headers: {
            'Content-Type': 'application/json',
        },        
    })
    .then(response => {
        if (!response.ok) {
            carregar.style.display = 'none'
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    //Resposta do servidor
    .then(data => {
            
        //Mostar a resposta
        if (data.toLowerCase().includes("verdade")) {

            
            resposta.style.color = "green"; // Altera a cor para verde
            
        } 
        else {
            resposta.style.color = "red"; // Altera a cor para vermelho
        }
            
        resposta.innerText = data
        carregar.style.display = 'none'
        enviar_IA.style.display = 'none'
   
    })  
    .catch(error => console.error('Erro:', error));  // Tratamento de erros
});


// Quando o usuário selecionar uma imagem
controla_css_input_imagem.addEventListener("change", function(event) {
    const file = event.target.files[0];
    if (file) {
        const leitor = new FileReader();
        leitor.onload = function(e) {
            previewImagem.src = e.target.result;
            previewImagem.style.display = "block";
            
        };
        leitor.readAsDataURL(file);
    } else {
        previewImagem.style.display = "none";
        previewImagem.src = "";
    }
});