/**
 * Insere um novo item na tabela de registros.
 * O item deve ser um objeto com as propriedades correspondentes às colunas da tabela.
 */
const insertRecord = (item) => {
    const tableBody = document.getElementById('records-table-body');
    const row = tableBody.insertRow();

    // Atribui um ID à linha para facilitar a remoção
    row.dataset.id = item.id;

    // Cria as células da tabela de forma segura
    const createCell = (html) => {
        const cell = row.insertCell();
        cell.innerHTML = html;
        return cell;
    };

    createCell(item.farmer);
    createCell(item.crop);
    createCell(item.size);
    createCell(item.weight);
    createCell(item.sweetness);
    createCell(item.crunchiness);
    createCell(item.juiciness);
    createCell(item.ripeness);
    createCell(item.acidity);

    const qualityMap = { 0: 'Bom', 1: 'Ruim' };
    const qualityText = qualityMap[item.quality] || 'N/A';
    const qualityCell = createCell(`<b>${qualityText}</b>`);

    // Adiciona uma classe CSS para estilização com base na qualidade
    if (item.quality === 0) {
        qualityCell.classList.add('quality-good');
    } else if (item.quality === 1) {
        qualityCell.classList.add('quality-bad');
    }

    // Cria o botão de deletar e adiciona o event listener
    const actionsCell = row.insertCell();
    const deleteButton = document.createElement('button');
    deleteButton.className = 'action-button';
    deleteButton.textContent = 'Deletar';
    deleteButton.onclick = () => {
        deleteRecord(item.id);
    };
    actionsCell.appendChild(deleteButton);
}

/**
 * Carrega todos os registros da API e os exibe na tabela.
 */
const loadRecords = async () => {
    const tableBody = document.getElementById('records-table-body');
    tableBody.innerHTML = ""; // Limpa a tabela antes de carregar novos dados
    try {
        // Usa a URL base da API do arquivo de configuração
        const response = await fetch(`${CONFIG.API_BASE_URL}/predictions`);
        if (!response.ok) {
            throw new Error('Falha ao buscar dados da API');
        }
        const data = await response.json();
        // A API retorna um objeto com uma chave "predictions" que é uma lista
        data.predictions.forEach(item => insertRecord(item));
    } catch (error) {
        console.error("Erro ao carregar registros:", error);
        alert("Não foi possível carregar os registros. Verifique a conexão com a API.");
    }
};

/**
 * Deleta um registro com base no seu ID.
 */
const deleteRecord = async (id) => {
    if (confirm(`Tem certeza que deseja deletar este registro?`)) {
        try {
            const response = await fetch(`${CONFIG.API_BASE_URL}/predictions?id=${id}`, { method: 'DELETE' });
            if (response.ok) {
                // Remove a linha da tabela da interface
                document.querySelector(`tr[data-id='${id}']`).remove();
                alert("Registro deletado com sucesso!");
            } else {
                const errorData = await response.json();
                alert(`Erro ao deletar: ${errorData.message}`);
            }
        } catch (error) {
            console.error("Erro ao deletar registro:", error);
            alert("Falha na comunicação com a API.");
        }
    }
};

// Adiciona o listener para o evento de submissão do formulário
document.getElementById('prediction-form').addEventListener('submit', async (event) => {
    event.preventDefault(); // Previne o comportamento padrão de submissão

    const form = event.target;
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());

    // Converte campos numéricos para o tipo float, pois JSON não tem tipo de formulário
    const numericFields = ['size', 'weight', 'sweetness', 'crunchiness', 'juiciness', 'ripeness', 'acidity'];
    numericFields.forEach(field => {
        if (data[field]) data[field] = parseFloat(data[field]);
    });

    try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/predictions`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data),
        });

        const resultDiv = document.getElementById('result');
        const resultData = await response.json();

        if (response.ok) {
            const qualityText = resultData.quality === 0 ? 'Bom' : 'Ruim';
            resultDiv.textContent = `A qualidade da maçã é: ${qualityText}`;
            resultDiv.style.backgroundColor = '#d4edda'; // Verde para sucesso
            loadRecords(); // Recarrega a tabela para mostrar o novo registro
            form.reset(); // Limpa o formulário
            // O modal não é mais fechado automaticamente para que o usuário veja a mensagem de sucesso.
        } else {
            resultDiv.textContent = `Erro: ${resultData.message}`;
            resultDiv.style.backgroundColor = '#f8d7da'; // Vermelho para erro
        }
    } catch (error) {
        console.error('Erro ao enviar o formulário:', error);
        document.getElementById('result').textContent = 'Erro de comunicação com a API.';
    }
});

// Carrega os registros iniciais quando a página é carregada
window.onload = () => {
    loadRecords();

    // --- Lógica para o Modal ---
    const modal = document.getElementById('form-modal');
    const openModalBtn = document.getElementById('open-modal-btn');
    const closeModalBtn = document.querySelector('.close-button');

    openModalBtn.onclick = () => modal.style.display = 'block';
    closeModalBtn.onclick = () => modal.style.display = 'none';

    window.onclick = (event) => {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    }
};