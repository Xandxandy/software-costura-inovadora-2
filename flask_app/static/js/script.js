function confirmarExclusao(tipo) {
    return confirm(
        "Tem certeza que deseja excluir este " + tipo + "?"
    );
}


// Busca o endereço automaticamente a partir do CEP
async function buscarEnderecoPorCep() {
    const campoCep = document.getElementById("cep");

    // Algumas páginas do sistema não possuem campo de CEP.
    // Nesse caso, a função simplesmente não faz nada.
    if (!campoCep) {
        return;
    }

    // Remove tudo que não for número.
    const cep = campoCep.value.replace(/\D/g, "");

    // Se o campo estiver vazio, não realiza a consulta.
    if (cep === "") {
        return;
    }

    // Um CEP brasileiro precisa ter 8 números.
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

        // O ViaCEP retorna erro = true quando o CEP não existe.
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

        // Depois de preencher o endereço,
        // coloca o cursor diretamente no número.
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


// Quando a página terminar de carregar
document.addEventListener("DOMContentLoaded", function () {
    const campoCep = document.getElementById("cep");

    if (campoCep) {

        // Consulta o CEP quando a pessoa sair do campo.
        campoCep.addEventListener("blur", buscarEnderecoPorCep);
    }
});