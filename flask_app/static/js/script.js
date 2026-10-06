// --------------------------------------------------
// Confirmação de exclusão
// --------------------------------------------------

function confirmarExclusao(tipo) {
    return confirm(
        "Tem certeza que deseja excluir este " + tipo + "?"
    );
}


// --------------------------------------------------
// ViaCEP
// --------------------------------------------------

// Busca o endereço automaticamente a partir do CEP.
async function buscarEnderecoPorCep() {
    const campoCep = document.getElementById("cep");

    // Algumas páginas não possuem campo de CEP.
    if (!campoCep) {
        return;
    }

    // Mantém somente os números.
    const cep = campoCep.value.replace(/\D/g, "");

    // Não consulta se o campo estiver vazio.
    if (cep === "") {
        return;
    }

    // CEP brasileiro possui 8 números.
    if (cep.length !== 8) {
        alert("Digite um CEP válido com 8 números.");
        return;
    }

    try {
        const resposta = await fetch(
            `https://viacep.com.br/ws/${cep}/json/`
        );

        if (!resposta.ok) {
            throw new Error("Erro ao consultar o CEP.");
        }

        const endereco = await resposta.json();

        // ViaCEP retorna erro = true quando o CEP não existe.
        if (endereco.erro) {
            alert("CEP não encontrado.");
            return;
        }

        document.getElementById("logradouro").value =
            endereco.logradouro || "";

        document.getElementById("bairro").value =
            endereco.bairro || "";

        document.getElementById("cidade").value =
            endereco.localidade || "";

        document.getElementById("uf").value =
            endereco.uf || "";

        // Após preencher o endereço, posiciona o cursor
        // no campo número.
        const campoNumero = document.getElementById("numero");

        if (campoNumero) {
            campoNumero.focus();
        }

    } catch (erro) {
        console.error("Erro ao consultar ViaCEP:", erro);

        alert(
            "Não foi possível consultar o CEP. Tente novamente."
        );
    }
}


// --------------------------------------------------
// Pesquisa e exibição de registros
// --------------------------------------------------

function configurarPesquisaRegistros(configuracao) {

    const campoPesquisa = document.getElementById(
        configuracao.idPesquisa
    );

    const botaoMostrar = document.getElementById(
        configuracao.idBotao
    );

    const lista = document.getElementById(
        configuracao.idLista
    );

    const mensagemPesquisa = document.getElementById(
        configuracao.idMensagem
    );

    const registros = document.querySelectorAll(
        configuracao.seletorItem
    );


    // Se os elementos não existirem nesta página,
    // a função não precisa executar.
    if (
        !campoPesquisa ||
        !botaoMostrar ||
        !lista ||
        !mensagemPesquisa
    ) {
        return;
    }


    // Pesquisa enquanto o usuário digita.
    campoPesquisa.addEventListener("input", function () {

        const pesquisa = campoPesquisa.value
            .toLowerCase()
            .trim();


        // Se a pesquisa for apagada,
        // volta ao estado inicial.
        if (pesquisa === "") {

            lista.hidden = true;
            mensagemPesquisa.hidden = true;

            botaoMostrar.textContent = "Mostrar todos";

            registros.forEach(function (registro) {
                registro.hidden = false;
            });

            return;
        }


        let encontrouRegistro = false;


        registros.forEach(function (registro) {

            const dadosRegistro = registro.textContent
                .toLowerCase();

            const corresponde = dadosRegistro.includes(
                pesquisa
            );

            registro.hidden = !corresponde;

            if (corresponde) {
                encontrouRegistro = true;
            }
        });


        // Durante uma pesquisa, exibe a lista.
        lista.hidden = false;

        // Exibe a mensagem apenas quando
        // nenhum registro for encontrado.
        mensagemPesquisa.hidden = encontrouRegistro;

        botaoMostrar.textContent = "Mostrar todos";
    });


    // Alterna entre mostrar e ocultar todos os registros.
    botaoMostrar.addEventListener("click", function () {

        const listaEstaOculta = lista.hidden;


        if (listaEstaOculta) {

            // Limpa uma eventual pesquisa.
            campoPesquisa.value = "";

            // Torna todos os registros visíveis.
            registros.forEach(function (registro) {
                registro.hidden = false;
            });

            lista.hidden = false;
            mensagemPesquisa.hidden = true;

            botaoMostrar.textContent = "Ocultar lista";

        } else {

            lista.hidden = true;
            mensagemPesquisa.hidden = true;

            campoPesquisa.value = "";

            botaoMostrar.textContent = "Mostrar todos";
        }
    });
}


// --------------------------------------------------
// Inicialização da página
// --------------------------------------------------

document.addEventListener("DOMContentLoaded", function () {

    // ViaCEP
    const campoCep = document.getElementById("cep");

    if (campoCep) {
        campoCep.addEventListener(
            "blur",
            buscarEnderecoPorCep
        );
    }


    // Clientes
    configurarPesquisaRegistros({
        idPesquisa: "pesquisa-cliente",
        idBotao: "mostrar-clientes",
        idLista: "lista-clientes",
        idMensagem: "mensagem-pesquisa",
        seletorItem: ".cliente-item"
    });


    // Serviços
    configurarPesquisaRegistros({
        idPesquisa: "pesquisa-servico",
        idBotao: "mostrar-servicos",
        idLista: "lista-servicos",
        idMensagem: "mensagem-pesquisa-servico",
        seletorItem: ".servico-item"
    });


    // Pedidos
    configurarPesquisaRegistros({
        idPesquisa: "pesquisa-pedido",
        idBotao: "mostrar-pedidos",
        idLista: "lista-pedidos",
        idMensagem: "mensagem-pesquisa-pedido",
        seletorItem: ".pedido-item"
    });


    // Orçamentos
    configurarPesquisaRegistros({
        idPesquisa: "pesquisa-orcamento",
        idBotao: "mostrar-orcamentos",
        idLista: "lista-orcamentos",
        idMensagem: "mensagem-pesquisa-orcamento",
        seletorItem: ".orcamento-item"
    });
});